#!/usr/bin/env bash
# Install or update the own-your-diff plugin in each harness named, or each one on PATH.
# OWN_YOUR_DIFF_SOURCE overrides the marketplace (a local clone path works).
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SOURCE=${OWN_YOUR_DIFF_SOURCE:-krimvp/own-your-diff}
ID=own-your-diff@own-your-diff

# Each step converges: a first run installs, a rerun updates to the latest release.
claude_install() {
  claude plugin marketplace add "$SOURCE" >/dev/null 2>&1 || true
  claude plugin marketplace update own-your-diff
  claude plugin install "$ID" --scope user
  claude plugin update "$ID" --scope user
  # A repo whose .claude/settings.json enables the plugin gets its own project-scope
  # install, which a user-scope update leaves on the old version.
  local project
  for project in $(claude_projects); do
    (cd "$project" && claude plugin update "$ID" --scope project)
  done
}

claude_projects() {
  python3 - "$ID" <<'PY'
import json, os, sys
path = os.path.expanduser("~/.claude/plugins/installed_plugins.json")
try:
    entries = json.load(open(path)).get("plugins", {}).get(sys.argv[1], [])
except (OSError, ValueError):
    entries = []
for entry in entries:
    if entry.get("scope") == "project" and os.path.isdir(entry.get("projectPath", "")):
        print(entry["projectPath"])
PY
}

droid_install() {
  droid plugin marketplace add "$SOURCE" >/dev/null 2>&1 || true
  droid plugin marketplace update own-your-diff
  droid plugin install "$ID" --scope user 2>/dev/null || droid plugin update "$ID" --scope user
}

codex_install() {
  codex plugin marketplace add "$SOURCE" >/dev/null 2>&1 || true
  codex plugin marketplace upgrade own-your-diff
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
