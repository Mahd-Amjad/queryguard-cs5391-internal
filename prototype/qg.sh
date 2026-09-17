#!/usr/bin/env bash
# QueryGuard one-command tool.
#   ./qg.sh          -> setup (first run) + tests + corpus gate (the quality check)
#   ./qg.sh serve    -> setup (first run) + start the web app on :5055
set -e
cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
    echo "[setup] creating environment (first run only)"
    python3 -m venv --system-site-packages .venv
fi
.venv/bin/pip install -q -r requirements.txt

case "${1:-check}" in
    check)
        .venv/bin/python -m pytest tests/ -q
        .venv/bin/python scripts/run_eval.py --corpus data/corpus.jsonl --fail-on-miss
        .venv/bin/python scripts/check_counts.py
        echo "ALL CHECKS PASSED"
        ;;
    serve)
        exec .venv/bin/python -m queryguard.app
        ;;
    *)
        echo "usage: ./qg.sh [check|serve]" >&2
        exit 2
        ;;
esac
