"""Corpus evaluation harness (FR-E1/E2/E3): run the labeled corpus, compare
verdicts, emit a report. --fail-on-miss exits 1 on any verdict mismatch (the
CI mechanical gate)."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from queryguard import db  # noqa: E402
from queryguard.gate import evaluate  # noqa: E402
from queryguard.generator import MockGenerator  # noqa: E402


def load_corpus(path: Path) -> list[dict]:
    entries = []
    for line in path.read_text().splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries


def evaluate_corpus(mode: str = "mock", corpus_path: Path | None = None) -> dict:
    if mode != "mock":
        raise NotImplementedError("live mode not configured; use mock mode")
    corpus_path = corpus_path or (ROOT / "data" / "corpus.jsonl")
    allowlist = json.loads((ROOT / "data" / "allowlist.json").read_text())
    gen = MockGenerator()
    conn = db.readonly_connection()
    table_columns = db.table_columns(conn)
    conn.close()

    results, mismatches = [], []
    latencies = []
    per_class = {}
    for entry in load_corpus(corpus_path):
        gen_out = gen.generate(entry["prompt"])
        t0 = time.perf_counter()
        result = evaluate(gen_out["sql"], allowlist, table_columns)
        latency = (time.perf_counter() - t0) * 1000
        latencies.append(latency)
        got, expected = result.verdict, entry["expected"]
        ok = got == expected or (expected == "BLOCK" and got == "MASK")
        row = {
            "id": entry["id"],
            "class": entry["class"],
            "expected": entry["expected"],
            "got": result.verdict,
            "rule": result.rule_id,
            "expected_rule": entry.get("expected_rule", ""),
            "ok": ok,
        }
        results.append(row)
        per_class.setdefault(entry["class"], {"n": 0, "blocked": 0, "masked": 0})
        per_class[entry["class"]]["n"] += 1
        if result.verdict == "BLOCK":
            per_class[entry["class"]]["blocked"] += 1
        if result.verdict == "MASK":
            per_class[entry["class"]]["masked"] += 1
        if result.verdict in ("BLOCK", "MASK"):
            per_class[entry["class"]].setdefault("safe", 0)
            per_class[entry["class"]]["safe"] += 1
        if not ok:
            mismatches.append(row)

    latencies.sort()
    p = lambda q: round(latencies[min(len(latencies) - 1, int(len(latencies) * q))], 3) if latencies else 0.0
    return {
        "mode": mode,
        "total": len(results),
        "matched": len(results) - len(mismatches),
        "mismatches": mismatches,
        "block_rate_by_class": {k: round(v["blocked"] / v["n"], 4) for k, v in per_class.items()},
        "masked_by_class": {k: v.get("masked", 0) for k, v in per_class.items()},
        "safe_rate_by_class": {k: round((v.get("blocked", 0) + v.get("masked", 0)) / v["n"], 4) for k, v in per_class.items()},
        "latency_p50_ms": p(0.50),
        "latency_p95_ms": p(0.95),
        "results": results,
    }


def write_report(report: dict, path: Path) -> None:
    path.parent.mkdir(exist_ok=True)
    lines = [
        "# QueryGuard evaluation report",
        f"- mode: {report['mode']}",
        f"- corpus entries: {report['total']}",
        f"- verdict matches: {report['matched']}/{report['total']}",
        f"- block rate by class: {json.dumps(report['block_rate_by_class'])}",
        f"- latency p50/p95 ms: {report['latency_p50_ms']} / {report['latency_p95_ms']}",
        "",
        "| id | class | expected | got | rule |",
        "|---|---|---|---|---|",
    ]
    for r in report["results"]:
        lines.append(f"| {r['id']} | {r['class']} | {r['expected']} | {r['got']} | {r['rule']} |")
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=str(ROOT / "data" / "corpus.jsonl"))
    ap.add_argument("--mode", choices=["mock"], default="mock")
    ap.add_argument("--report", default="")
    ap.add_argument("--fail-on-miss", action="store_true")
    args = ap.parse_args()

    report = evaluate_corpus(mode=args.mode, corpus_path=Path(args.corpus))
    print(json.dumps({k: v for k, v in report.items() if k != "results"}, indent=2))
    if args.report:
        write_report(report, Path(args.report))
        print(f"report written: {args.report}")
    if args.fail_on_miss and report["mismatches"]:
        print(f"FAIL: {len(report['mismatches'])} verdict mismatches", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
