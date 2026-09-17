#!/usr/bin/env python3
"""Truth-pass automation (QA_CHECKLIST "Truth pass", SM65): catches test-count
drift and stale rule-count language across the canonical files. Stdlib only.
Exits 1 on any finding so `qg.sh check` fails loudly. Pointer resolution and
dead-directive judgment stay with check-consistency / human review by design.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # prototype/
PROJECT = ROOT.parent                        # project/

CANONICAL = [
    "README.md", "INDEX.md", "TECH_PLAN.md", "srs/SRS.md",
    "prototype/README.md", "prototype/docs/story.md",
    "group/SRS_REVIEW.html", "submission/SUBMISSION_CHECKLIST.md",
]

STALE_LANGUAGE = [
    "nine rules", "nine safety", "nine core", "nine deterministic",
    "9 rules", "9 safety", "ten rules", "10 rules",
]

BACKEND_PATTERNS = [r"(\d+)\s+backend", r"(\d+)\s+automated tests", r"(\d+)\s+tests:"]
FRONTEND_PATTERNS = [r"(\d+)\s+frontend"]


def stated_counts(text: str, patterns: list[str]) -> set[str]:
    found: set[str] = set()
    for pattern in patterns:
        found.update(m.group(1) for m in re.finditer(pattern, text, re.I))
    return found


def main() -> int:
    findings: list[str] = []
    stated: dict[str, dict[str, set[str]]] = {"backend": {}, "frontend": {}}

    for rel in CANONICAL:
        path = PROJECT / rel
        if not path.exists():
            findings.append(f"missing canonical file: {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for needle in STALE_LANGUAGE:
            for lineno, line in enumerate(text.splitlines(), 1):
                if needle in line.lower():
                    findings.append(
                        f"stale rule language '{needle}' at {rel}:{lineno}: {line.strip()[:70]}"
                    )
        for kind, patterns in (("backend", BACKEND_PATTERNS), ("frontend", FRONTEND_PATTERNS)):
            values = stated_counts(text, patterns)
            if values:
                stated[kind][rel] = values

    for kind, per_file in stated.items():
        distinct = {v for values in per_file.values() for v in values}
        if len(distinct) > 1:
            detail = "; ".join(f"{f}: {sorted(v)}" for f, v in per_file.items())
            findings.append(f"inconsistent {kind} counts -> {detail}")

    if findings:
        print(f"check_counts: {len(findings)} finding(s)")
        for finding in findings:
            print(" -", finding)
        return 1
    print("check_counts: clean (counts consistent, no stale rule language)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
