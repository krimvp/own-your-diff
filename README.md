# own-your-diff

Push only what you can explain. Before a push, your agent writes an HTML walkthrough of the unpushed change and quizzes you on it. A git pre-push hook blocks commits that have no passed quiz.

One plugin tree serves Claude Code, Factory Droid, and Codex. Claude Code and Droid read `.claude-plugin/`. Codex reads its native `.codex-plugin/` and `.agents/plugins/marketplace.json`, which add its display name, category, and starter prompts. Each harness gets:

- The `own-your-diff` skill: walkthrough, quiz, and record steps, plus the `quizgate`, `snippet`, `plainlint` and `quizlint` tools. Walkthroughs follow a plain-English guide and explain from the whole system down to the code.
- A session-start hook. It keeps `quizgate` current in `~/.local/bin` and installs the git hook in any clone of an opted-in repo.
- A shell guard. It denies an agent's `git push --no-verify` and any `core.hooksPath` change. Skipping the gate is the human's call.

## Install

```bash
git clone https://github.com/krimvp/own-your-diff && own-your-diff/install.sh            # every harness on PATH
own-your-diff/install.sh codex                                                          # or name them
```

`install.sh` runs these. You can also run them by hand:

| Harness | Commands |
|---|---|
| Claude Code | `claude plugin marketplace add krimvp/own-your-diff`<br>`claude plugin install own-your-diff@own-your-diff` |
| Factory Droid | `droid plugin marketplace add krimvp/own-your-diff`<br>`droid plugin install own-your-diff@own-your-diff --scope user` |
| Codex | `codex plugin marketplace add krimvp/own-your-diff`<br>`codex plugin add own-your-diff@own-your-diff`<br>`scripts/codex-trust-hooks` |

Codex skips plugin hooks until you trust them. `scripts/codex-trust-hooks` writes the same trust entries the Codex TUI writes when you approve them. Rerun it after an update that changes `hooks/hooks.json`.

## Opt a repo in

```bash
quizgate install    # writes .own-your-diff and .git/hooks/pre-push
git add .own-your-diff && git commit -m "chore: require own-your-diff before push"
```

The committed `.own-your-diff` file is the opt-in. In a fresh clone, the plugin's session-start hook sees it and installs the git hook. `quizgate install` leaves an existing pre-push hook alone, and so does a repo whose `core.hooksPath` points at a hooks manager such as husky. Each time, it prints the line to add. A `core.hooksPath` that points at a missing directory, such as a deleted `.githooks`, is unset at the next session start.

To have Claude Code and Droid offer the plugin to everyone who opens the repo, commit this as `.claude/settings.json` and `.factory/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "own-your-diff": { "source": { "source": "github", "repo": "krimvp/own-your-diff" } }
  },
  "enabledPlugins": { "own-your-diff@own-your-diff": true }
}
```

## Without a plugin

Any agent that reads skills from `~/.agents/skills` can use the skill directly:

```bash
ln -s "$PWD/own-your-diff/skills/own-your-diff" ~/.agents/skills/own-your-diff
own-your-diff/skills/own-your-diff/scripts/quizgate sync
```

The git hook does not depend on any harness. It runs `quizgate` from `PATH` or `~/.local/bin`, and blocks with an install hint when it finds neither.

## Quiz evals

`evals/` measures the questions the skill writes, on real past changes, through [multeval](https://github.com/krimvp/multeval). See [`evals/README.md`](evals/README.md).

## Updating

Rerun `install.sh`. It refreshes each marketplace, updates the plugin, and re-trusts the Codex hooks. In Claude Code, it also updates each repo's project-scope install, which a repo's `.claude/settings.json` creates. Restart open sessions to load the new version.

Claude Code and Codex cache the plugin by its `version`. Bump it in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` with every change you want installs to pick up. The selftest fails when they differ.
