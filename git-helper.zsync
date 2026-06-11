#!/usr/bin/env bash
# git-helper.sh — Safe helpers: backport-cherry-pick, batch-revert
# Usage:
#   ./git-helper.sh backport <commit-sha> <target-branch>   # cherry-pick commit into target branch
#   ./git-helper.sh batch-revert <sha1,sha2,...> <target-branch>
#
# Notes:
# - Script requires git in PATH and you must run it inside a repo.
# - It will NOT force-push automatically. It creates a temporary branch and leaves the repo in a safe state.
# - On conflicts, it stops and prints next steps so you can resolve interactively.

set -euo pipefail

die() { echo "ERROR: $*"; exit 1; }
info() { echo "INFO: $*"; }

require_clean_worktree() {
  if ! git diff --quiet || ! git diff --cached --quiet; then
    die "Working tree or index not clean. Commit or stash changes before running this script."
  fi
}

fetch_origin() {
  info "Fetching origin..."
  git fetch origin --prune
}

create_temp_branch() {
  local base="$1"
  local tmp="tmp/$(date +%s)-$RANDOM"
  git checkout -b "$tmp" "$base"
  echo "$tmp"
}

backport_cherry_pick() {
  local sha="$1"
  local target="$2"

  require_clean_worktree
  fetch_origin

  info "Checking out target branch $target (from origin/$target)..."
  git checkout -B "$target" "origin/$target" || die "Failed to checkout origin/$target"

  local tmp
  tmp=$(create_temp_branch "$target")
  info "Temporary branch created: $tmp. Cherry-picking $sha ..."

  if git cherry-pick -x "$sha"; then
    info "Cherry-pick succeeded on $tmp. Review, run tests, then push:"
    echo "  git checkout $target"
    echo "  git merge --ff-only $tmp   # or 'git checkout $target; git merge $tmp'"
    echo "  git push origin $target"
  else
    echo
    die "Cherry-pick failed with conflicts. Resolve conflicts, then run: git cherry-pick --continue  OR to abort: git cherry-pick --abort"
  fi
}

batch_revert() {
  local shalist_csv="$1"
  local target="$2"

  require_clean_worktree
  fetch_origin

  info "Checking out target branch $target (from origin/$target)..."
  git checkout -B "$target" "origin/$target" || die "Failed to checkout origin/$target"

  local tmp
  tmp=$(create_temp_branch "$target")
  info "Temporary branch created: $tmp. Beginning batch revert..."

  IFS=',' read -ra SHAS <<< "$shalist_csv"
  for sha in "${SHAS[@]}"; do
    sha=$(echo "$sha" | xargs)  # trim
    info "Reverting $sha ..."
    if git revert --no-edit "$sha"; then
      info "Reverted $sha"
    else
      die "Revert of $sha failed with conflicts. Resolve conflicts, then run 'git revert --continue' or 'git revert --abort'. Branch $tmp contains the current state."
    fi
  done

  info "All requested reverts applied on $tmp. Review changes, run tests, then push:"
  echo "  git checkout $target"
  echo "  git merge --ff-only $tmp   # or 'git checkout $target; git merge $tmp'"
  echo "  git push origin $target"
}

if [ "${#@}" -lt 1 ]; then
  die "No operation specified. Usage: $0 {backport|batch-revert} ..."
fi

op="$1"; shift
case "$op" in
  backport)
    if [ "$#" -ne 2 ]; then
      die "Usage: $0 backport <commit-sha> <target-branch>"
    fi
    backport_cherry_pick "$1" "$2"
    ;;
  batch-revert)
    if [ "$#" -ne 2 ]; then
      die "Usage: $0 batch-revert <sha1,sha2,...> <target-branch>"
    fi
    batch_revert "$1" "$2"
    ;;
  *)
    die "Unknown op: $op. Supported: backport, batch-revert"
    ;;
esac
