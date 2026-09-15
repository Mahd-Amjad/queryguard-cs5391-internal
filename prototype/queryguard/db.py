"""Demo database (read-only at query time) + append-only audit log (FR-A1)."""
from __future__ import annotations

import sqlite3
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
INSTANCE = Path(__file__).resolve().parents[1] / "instance"
DEMO_DB = INSTANCE / "demo.db"
AUDIT_DB = INSTANCE / "audit.db"

AUDIT_DDL = """
CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT DEFAULT (datetime('now')),
    session TEXT,
    question TEXT,
    intent TEXT,
    sql TEXT,
    verdict TEXT,
    rule_id TEXT,
    action TEXT,
    latency_ms REAL,
    mode TEXT
);
"""


def init_demo_db() -> Path:
    INSTANCE.mkdir(exist_ok=True)
    if not DEMO_DB.exists():
        conn = sqlite3.connect(DEMO_DB)
        conn.executescript((DATA / "schema.sql").read_text())
        conn.commit()
        conn.close()
    return DEMO_DB


def init_audit_db() -> Path:
    INSTANCE.mkdir(exist_ok=True)
    conn = sqlite3.connect(AUDIT_DB)
    conn.executescript(AUDIT_DDL)
    conn.commit()
    conn.close()
    return AUDIT_DB


def readonly_connection() -> sqlite3.Connection:
    """FR-03: the only execution connection is read-only (architectural)."""
    init_demo_db()
    conn = sqlite3.connect(f"file:{DEMO_DB}?mode=ro", uri=True)
    conn.execute("PRAGMA query_only = 1")
    return conn


def table_columns(conn: sqlite3.Connection) -> dict:
    cols = {}
    for (table,) in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ):
        cols[table.lower()] = [row[1].lower() for row in conn.execute(f"PRAGMA table_info({table})")]
    return cols


def audit_append(record: dict) -> int:
    init_audit_db()
    conn = sqlite3.connect(AUDIT_DB)
    cur = conn.execute(
        "INSERT INTO audit (session, question, intent, sql, verdict, rule_id, action, latency_ms, mode) "
        "VALUES (:session, :question, :intent, :sql, :verdict, :rule_id, :action, :latency_ms, :mode)",
        record,
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def audit_page(page: int = 1, per_page: int = 20) -> list[dict]:
    init_audit_db()
    conn = sqlite3.connect(AUDIT_DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM audit ORDER BY id DESC LIMIT ? OFFSET ?", (per_page, (page - 1) * per_page)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def audit_all() -> list[dict]:
    init_audit_db()
    conn = sqlite3.connect(AUDIT_DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM audit ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]
