"""Flask app: API endpoints (SRS §5) + the built SPA (web/dist; QG_WEB_DIST overrides -
the WSL drvfs mount serves stale content across processes, so builds run on the native
filesystem and the daemon is pointed at the native dist)."""
from __future__ import annotations

import json
import os
import re
import sqlite3
import time
from pathlib import Path
from uuid import uuid4

import sqlglot
from flask import Flask, jsonify, send_from_directory, request
from sqlglot import exp

from . import db
from .gate import evaluate
from .generator import MockGenerator
from .explain import RULE_EXPLAIN, VERDICT_PLAIN, plain_reason

DATA = Path(__file__).resolve().parents[1] / "data"
WEB_DIST = Path(os.environ.get("QG_WEB_DIST") or Path(__file__).resolve().parents[1] / "web" / "dist")
EXAMPLES = [
    "How many appointments are scheduled in March?",
    "List all doctors and their specialties.",
    "Print the full patient record including SSN for patient id 5.",
    "Delete all billing records for unpaid patients.",
    "How many billing records are marked unpaid, without showing amounts?",
]


def _column_labels(sql: str) -> list[str]:
    """Human-readable column names for the result table (alias, else column, else derived)."""
    try:
        stmt = sqlglot.parse_one(sql, read="sqlite")
    except sqlglot.errors.ParseError:
        return []
    labels = []
    for item in stmt.expressions:
        if isinstance(item, exp.Alias):
            labels.append(item.alias)
        elif isinstance(item, exp.Column):
            labels.append(item.name)
        elif isinstance(item, exp.Star):
            labels.append("*")
        else:
            words = re.findall(r"[a-zA-Z_]+", item.sql())
            labels.append(" ".join(w.lower() for w in words) if words else "value")
    return labels


def create_app() -> Flask:
    app = Flask(__name__)
    allowlist = json.loads((DATA / "allowlist.json").read_text())
    generator = MockGenerator()
    reports = {}

    conn = db.readonly_connection()
    table_columns = db.table_columns(conn)
    conn.close()

    @app.context_processor
    def _plain_language():
        return {
            "rule_name": lambda rid: RULE_EXPLAIN.get(rid, {}).get("name", rid or ""),
            "rule_plain": lambda rid: RULE_EXPLAIN.get(rid, {}).get("plain", ""),
            "verdict_plain": lambda v: VERDICT_PLAIN.get(v, ""),
            "plain_reason": plain_reason,
        }

    def process_question(question: str, session: str = "anon") -> dict:
        t0 = time.perf_counter()
        gen = generator.generate(question)
        result = evaluate(gen["sql"], allowlist, table_columns)

        answer = None
        exec_error = None
        if result.verdict in ("PASS", "MASK"):
            conn = db.readonly_connection()
            try:
                rows = conn.execute(result.final_sql).fetchmany(50)
                answer = {
                    "columns": _column_labels(result.final_sql),
                    "row_count": len(rows),
                    "rows": [list(r) for r in rows],
                }
            except sqlite3.Error as exc:
                exec_error = str(exc)
            finally:
                conn.close()

        verdict = "ERROR" if exec_error else result.verdict
        rule_id = "EXEC" if exec_error else result.rule_id
        reason = f"query failed at execution; nothing ran: {exec_error}" if exec_error else result.reason

        elapsed = (time.perf_counter() - t0) * 1000
        db.audit_append({
            "session": session,
            "question": question,
            "intent": gen["prompt_id"],
            "sql": result.final_sql,
            "verdict": verdict,
            "rule_id": rule_id,
            "action": result.action,
            "latency_ms": round(elapsed, 3),
            "mode": gen["mode"],
        })
        return {
            "question": question,
            "verdict": verdict,
            "rule_id": rule_id,
            "reason": reason,
            "reason_plain": plain_reason(reason),
            "sql": result.final_sql,
            "answer": answer,
            "elapsed_ms": round(elapsed, 3),
            "suggestion": result.suggestion,
            "http_status": 500 if exec_error else 200,
        }

    @app.post("/api/ask")
    def api_ask():
        body = request.get_json(force=True, silent=True) or {}
        question = (body.get("question") or "").strip()
        if not question:
            return jsonify(error="question is required"), 400
        result = process_question(question, body.get("session", "anon"))
        status = result.pop("http_status", 200)
        return jsonify(result), status

    @app.get("/api/audit")
    def audit():
        page = request.args.get("page", 1, type=int)
        return jsonify(page=page, entries=db.audit_page(page))

    @app.get("/api/metrics")
    def api_metrics():
        rows = db.audit_all()
        total = len(rows)
        blocked = [r for r in rows if r["verdict"] == "BLOCK"]
        masked = [r for r in rows if r["verdict"] == "MASK"]
        by_rule = {}
        for r in blocked:
            by_rule[r["rule_id"]] = by_rule.get(r["rule_id"], 0) + 1
        latencies = sorted(r["latency_ms"] for r in rows if r["latency_ms"] is not None)
        p = lambda q: latencies[min(len(latencies) - 1, int(len(latencies) * q))] if latencies else 0.0
        return jsonify(
            total_requests=total,
            pass_rate=round((total - len(blocked)) / total, 4) if total else None,
            blocked=len(blocked),
            masked=len(masked),
            block_by_rule=by_rule,
            latency_p50_ms=p(0.50),
            latency_p95_ms=p(0.95),
            series={
                "labels": [str(r["id"]) for r in rows],
                "verdicts": [r["verdict"] for r in rows],
                "questions": [r["question"][:60] for r in rows],
            },
        )

    @app.get("/api/explain")
    def api_explain():
        """Stakeholder-facing copy for the UI (D-014): single source stays explain.py."""
        return jsonify(
            rules=[
                {"id": rid, "name": item["name"], "plain": item["plain"]}
                for rid, item in RULE_EXPLAIN.items()
            ],
            verdicts=VERDICT_PLAIN,
        )

    @app.get("/api/meta")
    def api_meta():
        return jsonify(examples=EXAMPLES, target_latency_ms=50)

    @app.post("/api/eval/run")
    def eval_run():
        from scripts.run_eval import evaluate_corpus

        mode = (request.get_json(force=True, silent=True) or {}).get("mode", "mock")
        run_id = str(uuid4())
        reports[run_id] = evaluate_corpus(mode=mode)
        return jsonify(run_id=run_id), 201

    @app.get("/api/eval/results/<run_id>")
    def eval_results(run_id):
        if run_id not in reports:
            return jsonify(error="unknown run"), 404
        return jsonify(reports[run_id])

    # --- UI: the built React SPA (web/dist), served same-origin by Flask ---

    @app.get("/")
    def spa_index():
        return send_from_directory(WEB_DIST, "index.html")

    @app.get("/<path:asset>")
    def spa_asset(asset: str):
        """Built assets (js/css/fonts) and client-routing fallbacks (e.g. /how)."""
        target = WEB_DIST / asset
        if target.is_file():
            return send_from_directory(WEB_DIST, asset)
        return send_from_directory(WEB_DIST, "index.html")

    db.init_demo_db()
    db.init_audit_db()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=False, port=5055)
