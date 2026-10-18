#!/usr/bin/env bash
# Install the own-your-diff plugin into each harness named, or each one on PATH.
# OWN_YOUR_DIFF_SOURCE overrides the marketplace (a local clone path works).
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SOURCE=${OWN_YOUR_DIFF_SOURCE:-krimvp/own-your-diff}
ID=own-your-diff@own-your-diff

claude_install() {
  claude plugin marketplace add "$SOURCE" || claude plugin marketplace update own-your-diff
  claude plugin install "$ID" --scope user
}

droid_install() {
  droid plugin marketplace add "$SOURCE" || droid plugin marketplace update own-your-diff
  droid plugin install "$ID" --scope user
}

codex_install() {
  codex plugin marketplace add "$SOURCE" || codex plugin marketplace upgrade own-your-diff
  codex plugin add "$ID"
  "$HERE/scripts/codex-trust-hooks"
}

harnesses=("$@")
if ((${#harnesses[@]} == 0)); then
  for h in claude droid codex; do command -v "$h" >/dev/null && harnesses+=("$h"); done
fi
for h in "${harnesses[@]}"; do
  case "$h" in
    claude | droid | codex) echo "== $h"; "${h}_install" ;;
    *) echo "unknown harness: $h (claude, droid, codex)" >&2; exit 2 ;;
  esac
done
"$HERE/skills/own-your-diff/scripts/quizgate" sync
echo "quizgate is in ${QUIZGATE_BIN:-$HOME/.local/bin}. Opt a repo in with: quizgate install"
