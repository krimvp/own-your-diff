# AGENTS.md

One plugin tree for Claude Code, Factory Droid, and Codex. All three read `.claude-plugin/` and `hooks/hooks.json`, so there is one copy of each, not one per harness.

- Run `scripts/selftest` after changing anything under `skills/` or `hooks/`. It drives the gate through real `git push` and feeds the guard each harness's tool name.
- Run `claude plugin validate .` after changing a manifest.
- Bump `version` in `.claude-plugin/plugin.json` with every change that installs should pick up. Claude Code and Codex cache by it.
- Hook scripts find the plugin root with `dirname "$0"`. Droid sets `CLAUDE_PLUGIN_ROOT` to a placeholder inside hook processes, so they never read it from the environment.
- Editing `hooks/hooks.json` changes its Codex trust hash. Say in the change that Codex users must rerun `scripts/codex-trust-hooks`.
