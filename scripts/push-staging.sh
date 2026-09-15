#!/usr/bin/env bash
# push-staging.sh - one-shot: force-push the squashed staging main to the shared repo.
set -euo pipefail
cd "$HOME/repos/queryguard-cs5391"
git push -f origin main
echo "force-pushed squashed main to queryguard-cs5391"
