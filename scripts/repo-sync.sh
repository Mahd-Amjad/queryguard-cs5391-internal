#!/usr/bin/env bash
# repo-sync.sh - THE one tool for all QueryGuard repo pushes (nothing else pushes).
#
# Subcommands:
#   internal        push the full project tree (project/.git -> queryguard-cs5391-internal)
#   shared          converge the shared repo to submission/SHARED_WHITELIST.txt and push
#                   (queryguard-cs5391; frontend files there are Arwa's lane)
#   shared-dry      show what the shared convergence would change, commit nothing
#   both            internal, then shared
#
# Rules enforced here (do not push by hand):
#   - shared gets ONLY the whitelist paths; internal-only files never reach it
#   - commits are made here, small and labeled; no history rewrites without the operator
set -euo pipefail

PROJECT="/mnt/c/Users/Mahd/Videos/Work/Graduate/Texas_State/Semester_2_Fall_2026/CS5391_Software_Engineering/project"
STAGE_SHARED="$HOME/repos/queryguard-cs5391"
REMOTE_INTERNAL="git@github-personal:Mahd-Amjad/queryguard-cs5391-internal.git"
REMOTE_SHARED="git@github-personal:Mahd-Amjad/queryguard-cs5391.git"

push_internal() {
  git -C "$PROJECT" add -A
  if git -C "$PROJECT" diff --cached --quiet HEAD 2>/dev/null && [ -z "$(git -C "$PROJECT" status --porcelain)" ]; then
    echo "internal: nothing new"
  else
    git -C "$PROJECT" add -A
    git -C "$PROJECT" commit -q -m "internal snapshot $(date +%Y-%m-%d %H:%M)"
  fi
  if ! git -C "$PROJECT" remote | grep -q "^origin"; then
    git -C "$PROJECT" remote add origin "$REMOTE_INTERNAL"
  fi
  git -C "$PROJECT" push -u origin main
  echo "internal: pushed to queryguard-cs5391-internal"
}

converge_shared() {
  git -C "$STAGE_SHARED" fetch origin 2>/dev/null || true
  git -C "$STAGE_SHARED" reset --hard origin/main
  find "$STAGE_SHARED" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
  while IFS= read -r entry; do
    [ -z "$entry" ] && continue
    case "$entry" in \#*) continue ;; esac
    src="$PROJECT/prototype/$entry"
    if [ -e "$src" ]; then
      mkdir -p "$STAGE_SHARED/$entry"
      cp -r "$src/." "$STAGE_SHARED/$entry/" 2>/dev/null || cp -r "$src" "$STAGE_SHARED/$entry"
    else
      echo "WHITELIST-MISS: $entry" >&2
    fi
  done <<'WL'
README.md
qg.sh
requirements.txt
queryguard/
tests/
data/
scripts/
presentation/
.github/workflows/
docs/SRS.md
docs/SRS.html
docs/SRS.docx
docs/story.md
web/src/
web/public/
web/index.html
web/package.json
web/pnpm-lock.yaml
web/vite.config.ts
web/tsconfig.json
web/tsconfig.app.json
web/tsconfig.node.json
web/eslint.config.js
web/components.json
web/.env.example
web/.gitignore
WL
  git -C "$STAGE_SHARED" add -A
}

push_shared() {
  converge_shared
  if git -C "$STAGE_SHARED" diff --cached --quiet; then
    echo "shared: already up to date"
  else
    git -C "$STAGE_SHARED" commit -q -m "sync: publish whitelisted state from internal ($(date +%Y-%m-%d))"
    git -C "$STAGE_SHARED" push origin main
    echo "shared: pushed whitelisted state to queryguard-cs5391"
  fi
}

case "${1:-help}" in
  internal) push_internal ;;
  shared)   push_shared ;;
  both)     push_internal; push_shared ;;
  *) echo "usage: repo-sync.sh [internal|shared|both]"; exit 1 ;;
esac
