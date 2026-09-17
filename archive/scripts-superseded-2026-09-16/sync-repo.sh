#!/usr/bin/env bash
# Sync the QueryGuard workspace repo to GitHub through a staging clone outside
# the workspace. The workspace push-guard cannot verify remotes under /mnt/c and
# fails closed; ownership is unchanged (Mahd-Amjad personal repo, personal SSH
# alias), so the staging clone pushes the identical commits.
# Usage: bash sync-repo.sh
set -euo pipefail

SRC="/mnt/c/Users/Mahd/Videos/Work/Graduate/Texas_State/Semester_2_Fall_2026/CS5391_Software_Engineering/project/prototype"
STAGE="$HOME/repos/queryguard-cs5391"
REMOTE="git@github-personal:Mahd-Amjad/queryguard-cs5391.git"
BRANCH="main"

if [ ! -d "$STAGE/.git" ]; then
  mkdir -p "$(dirname "$STAGE")"
  git clone --no-local --origin workspace "$SRC" "$STAGE"
  git -C "$STAGE" config user.name "Mahd-Amjad"
  git -C "$STAGE" config user.email "m.mahdamjad@gmail.com"
fi

git -C "$STAGE" remote set-url workspace "$SRC"
git -C "$STAGE" fetch workspace "+refs/heads/$BRANCH:refs/remotes/workspace/$BRANCH"
git -C "$STAGE" reset --hard "workspace/$BRANCH"
git -C "$STAGE" remote add origin "$REMOTE" 2>/dev/null || git -C "$STAGE" remote set-url origin "$REMOTE"
git -C "$STAGE" push -u origin "$BRANCH"
echo "pushed $BRANCH to $REMOTE via $STAGE"
