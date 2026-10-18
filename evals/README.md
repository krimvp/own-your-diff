# Quiz evals

These evals measure the questions the skill writes, not the person answering them. Each case is a real change from this repo or from aigent, frozen with its unpushed commits. The agent plans the quiz for it, and the plan in `quiz.json` is graded.

Every attempt gets three grades:

- **`plan`, a script in multeval.** `quizlint --plan` must pass, and the question count and altitude must fit the case. A version bump gets no questions. A large design change gets no more than 10.
- **`trace`, in multeval.** Did the agent load the skill?
- **The judge, `evals/judge.py`, after the run.** A model checks each plan against its case's rubric. Every question targets the change, sits at the case's altitude, and skips the incidental parts. Wrong options are believable. Key points match the question's altitude. The last question applies the change to a new case. It writes `judge.json` beside each attempt.

multeval's own judge would be the natural home for the last grade. It relies on the endpoint enforcing a JSON schema, and Ollama Cloud ignores that ([multeval#24](https://github.com/krimvp/multeval/issues/24)). `evals/build --multeval-judge PROVIDER:MODEL` adds it back for an endpoint that does enforce one.

## Commands

Run every command from the repo root. Each needs Docker, `uv`, and SSH access to krimvp/multeval.

```bash
evals/eval prove              # fixed good and bad plans through the plan check: no model, no cost
evals/eval run                # pi on GLM 5.3 over Ollama Cloud, every case, then the judge
evals/eval compare main       # the skill at main against the working tree, 2 trials each
evals/eval judge evals/runs/<run>
evals/eval report evals/runs/<run>
skills/own-your-diff/scripts/quizstats evals/runs/<run>   # questions by category and kind
```

`prove` passes only when every good plan passes the `plan` check and every bad plan fails it. Run it after you change a check or a case. `run` and `compare` refuse to start until every subject and the judge have a key, because multeval itself would start them and record an unauthenticated session as completed ([multeval#21](https://github.com/krimvp/multeval/issues/21)).

## Subjects

- `run-ollama.json`, the default, is pi on `ollamacloud/glm-5.3`. It needs only an Ollama Cloud key.
- `run.json` is Claude Code on Sonnet 5.5. It needs `CLAUDE_CODE_OAUTH_TOKEN` (from `claude setup-token`) or `ANTHROPIC_API_KEY`. Claude Code cannot be pointed at Ollama Cloud yet ([multeval#25](https://github.com/krimvp/multeval/issues/25)).
- `run-harnesses.json` is Claude Code and Codex. Codex needs `OPENAI_API_KEY`.
- Droid is not a subject yet. multeval's Droid adapter runs on the host and takes no case environment, and each case here builds its git fixture in Docker ([multeval#22](https://github.com/krimvp/multeval/issues/22)).

## Keys

`evals/eval` loads `evals/.env`, which git ignores. It is a shell file, so it can read a key from another private file instead of copying it:

```bash
OLLAMA_API_KEY="$(sed -n 's/^OLLAMA_API_KEY=//p' "$HOME/workspace/aigent/.env")"
OPENAI_API_KEY="$OLLAMA_API_KEY"         # the judge
OPENAI_BASE_URL=https://ollama.com/v1
```

The judge model is `glm-5.3`. Set `JUDGE_MODEL` to use another model on the same endpoint.

## Cases

`cases.json` is the source. `evals/build` turns it into `suite/` and `oracle/`. Never edit those by hand. A case names its repo, the `base` and `head` of the change, the altitudes that fit it, the question range, the target, and the incidental parts. The rubric of the judge is written from the target, the altitude, and the incidental parts.

To add a case, add a row and run `evals/eval build`, then `evals/eval prove`. The aigent cases read the aigent repo from `../aigent`. Pass `--repo aigent=PATH` to `evals/build` when it lives elsewhere.

## multeval

`requirements.txt` follows multeval `main`. `requirements.lock.txt` pins the commit the evals last ran on. `evals/eval lock` moves the pin to the current `main`.
