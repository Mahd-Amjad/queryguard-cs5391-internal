"""Metamorphic testing for the gate (evaluation-depth unit).

Metamorphic relations: semantically equivalent rewrites of a candidate query
must not change the gate's verdict. Verdicts are compared (PASS/BLOCK/MASK);
rule attribution is deliberately not compared (D-006: attribution may shift
between equivalent defenses; D-003: adding a LIMIT legitimately clears G-09).

  MR-1 upper         : upper-casing the statement changes nothing
  MR-2 lower         : lower-casing the statement changes nothing
  MR-3 newlines      : newline separators between tokens change nothing
  MR-4 semicolon     : adding / removing the trailing semicolon changes nothing
  MR-5 add-limit     : appending LIMIT 5 to a SELECT changes nothing

Exit code 1 if any relation is violated; every violation is printed.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from queryguard import db  # noqa: E402
from queryguard.gate import evaluate  # noqa: E402
from queryguard.generator import MockGenerator  # noqa: E402


def _upper(sql: str) -> str:
    return sql.upper()


def _lower(sql: str) -> str:
    return sql.lower()


def _newlines(sql: str) -> str:
    return re.sub(r"[ \t]+", "\n", sql.strip())


def _add_semi(sql: str) -> str:
    return sql.rstrip().rstrip(";") + ";"


def _drop_semi(sql: str) -> str:
    return sql.rstrip().rstrip(";")


def _add_limit(sql: str) -> str:
    s = sql.rstrip().rstrip(";")
    if re.match(r"(?is)^\s*SELECT\b", s) and "LIMIT" not in s.upper():
        return s + " LIMIT 5;"
    return sql


MRS = {
    "MR-1-upper": _upper,
    "MR-2-lower": _lower,
    "MR-3-newlines": _newlines,
    "MR-4-semicolon": _add_semi,
    "MR-4b-no-semicolon": _drop_semi,
    "MR-5-add-limit": _add_limit,
}


def run() -> tuple[list[tuple], int]:
    allow = json.loads((ROOT / "data" / "allowlist.json").read_text())
    conn = db.readonly_connection()
    table_columns = db.table_columns(conn)
    conn.close()
    gen = MockGenerator()
    corpus = [json.loads(line) for line in (ROOT / "data" / "corpus.jsonl").read_text().splitlines() if line.strip()]

    violations: list[tuple] = []
    checked = 0
    for entry in corpus:
        sql = gen.generate(entry["prompt"])["sql"]
        base = evaluate(sql, allow, table_columns)
        for name, fn in MRS.items():
            checked += 1
            got = evaluate(fn(sql), allow, table_columns)
            if got.verdict != base.verdict:
                violations.append((entry["id"], name, base.verdict, got.verdict))
    return violations, checked


def main() -> int:
    violations, checked = run()
    print(f"metamorphic relations checked: {checked}")
    if violations:
        print(f"VIOLATIONS: {len(violations)}")
        for entry_id, name, base, got in violations:
            print(f"  {entry_id} {name}: {base} -> {got}")
        return 1
    print("all relations hold: equivalent rewrites never change the verdict")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
