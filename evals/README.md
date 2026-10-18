# Quiz evals

These evals measure the questions the skill writes, not the person answering them. Each case is a real change from this repo or from aigent, frozen with its unpushed commits. The agent plans the quiz for it, and multeval grades the plan in `quiz.json`.

Two checks grade every case:

- **`plan`, a script.** `quizlint --plan` must pass, and the question count and altitude must fit the case. A version bump gets no questions. A large design change gets no more than 10.
- **`judge`, a model.** It checks that every question targets the change, sits at the case's altitude, and skips the case's incidental parts. It also checks that wrong options are believable and that the last question applies the change to a new case.

A trace check also records whether the agent loaded the skill.

## Commands

Run every command from the repo root. Each needs Docker, `uv`, and SSH access to krimvp/multeval.

```bash
evals/eval prove              # fixed good and bad plans through the checks: no model, no cost
evals/eval run                # Claude Code on every case (evals/run.json)
evals/eval run evals/run-harnesses.json   # Claude Code and Codex
evals/eval compare main       # the skill at main against the working tree, 2 trials each
evals/eval report evals/runs/<run>
skills/own-your-diff/scripts/quizstats evals/runs/<run>   # questions by category and kind
```

`prove` passes only when every good plan passes the `plan` check and every bad plan fails it. Run it after you change a check or a case. `run` and `compare` refuse to start until every subject and the judge have a key, because multeval itself would start them and record an unauthenticated session as completed ([multeval#21](https://github.com/krimvp/multeval/issues/21)).

Droid is not a subject yet. multeval's Droid adapter runs on the host and takes no case environment, and each case here builds its git fixture in Docker ([multeval#22](https://github.com/krimvp/multeval/issues/22)).

## Keys

Put the keys in `evals/.env`, which git ignores. `evals/eval` loads it.

```bash
CLAUDE_CODE_OAUTH_TOKEN=...   # from `claude setup-token`, or ANTHROPIC_API_KEY
ANTHROPIC_API_KEY=...         # the judge; see below for another provider
OPENAI_API_KEY=...            # Codex subject
```

The judge defaults to `claude-opus-5-5` through the Anthropic API. For an OpenAI-compatible endpoint, rebuild with `evals/build --judge-provider openai --judge-model <id>`, and set `OPENAI_API_KEY` and `OPENAI_BASE_URL`.

## Cases

`cases.json` is the source. `evals/build` turns it into `suite/` and `oracle/`. Never edit those by hand. A case names its repo, the `base` and `head` of the change, the altitudes that fit it, the question range, the target, and the incidental parts.

To add a case, add a row and run `evals/eval build`. Then run `evals/eval prove`. The aigent cases read the aigent repo from `../aigent`. Pass `--repo aigent=PATH` to `evals/build` when it lives elsewhere.

## multeval

`requirements.txt` follows multeval `main`. `requirements.lock.txt` pins the commit the evals last ran on. `evals/eval lock` moves the pin to the current `main`.
