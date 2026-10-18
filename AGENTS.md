# AGENTS.md

One plugin tree for Claude Code, Factory Droid, and Codex. They share `skills/` and `hooks/hooks.json`. Claude Code and Droid read `.claude-plugin/`. Codex reads `.codex-plugin/` and `.agents/plugins/marketplace.json` first, for its listing metadata.

- Run `scripts/selftest` after changing anything under `skills/` or `hooks/`. It drives the gate through real `git push` and feeds the guard each harness's tool name.
- Run `claude plugin validate . --strict` after changing a manifest.
- CI (`.github/workflows/check.yml`) runs both on every push and PR.
- Bump `version` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` together with every change that installs should pick up. Claude Code and Codex cache by it.
- Hook scripts find the plugin root with `dirname "$0"`. Droid sets `CLAUDE_PLUGIN_ROOT` to a placeholder inside hook processes, so they never read it from the environment.
- Editing `hooks/hooks.json` changes its Codex trust hash. Say in the change that Codex users must rerun `scripts/codex-trust-hooks`.
- This repo stays out of its own gate while the walkthrough and quiz are still changing, so there is no `.own-your-diff` here. Leave it out until the human opts this repo in.
