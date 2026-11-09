# Quiz evals

These evals measure the questions the skill writes, not the person answering them. Each case is a real change from this repo or from aigent, frozen with its unpushed commits. The agent plans the quiz for it, and multeval grades the plan in `quiz.json`.

multeval holds every grade. `multeval report` shows them, `multeval compare` compares two runs, and `evals/QUALITY.md` tracks them over time.

## Checks

Every attempt gets five grades:

- **`plan`, a script.** `quizlint --plan` must pass, and the question count and altitude must fit the case. A version bump gets no questions. A large design change gets no more than 10.
- **`plain`, an exec grader.** `plain_grade.py` measures the words of the plan with the logic of `quizlint --json`. It scores the questions, the mean and longest prompt and option, code names per question, give-away options, and filler words. Lower is better for each. An attempt with no `quiz.json` gets no score.
- **`judge`, multeval's judge.** A model checks the plan against one rubric. The case's own facts sit in `check/brief.md`, which the judge reads as a hidden reference file. Every question targets the change, sits at the case's altitude, and skips the incidental parts. Wrong options are believable. Key points match the question's altitude. The last question applies the change to a new case. A person who knows the change can answer with the code closed. The words are plain English.
- **`trace`.** Did the agent load the skill?
- **`usage`.** Input and output tokens and the duration of the attempt.

The judge model is `glm-5.3` on Ollama Cloud. `evals/build --judge-model MODEL` picks another model on the same endpoint.

## Commands

Run every command from the repo root. Each needs Docker and `uv`. Without `MULTEVAL_SRC`, each also needs SSH access to krimvp/multeval.

```bash
evals/eval prove                    # fixed plans through the free checks: no model, no cost
evals/eval run                      # pi on GLM 5.3 over Ollama Cloud, every case, every check
evals/eval compare main             # the skill at main against the working tree, 2 trials each
evals/eval report evals/runs/<run>  # every grade of a run
evals/eval gate evals/runs/<run>    # the report, failing when a mean misses the bar
evals/eval diff evals/runs/<a> evals/runs/<b>   # two runs, metric by metric
evals/eval regrade evals/runs/<run> # grade a run again with today's plain, judge, trace, and usage
evals/eval keep evals/runs/<run>    # the trimmed run in evals/results/<run>, to commit
evals/eval quality                  # evals/QUALITY.md again, from evals/results
evals/eval lint                     # multeval's skill lint over skills/
skills/own-your-diff/scripts/quizstats evals/runs/<run>   # questions by category and kind
```

`prove` runs three fixed plan sets. A good plan has the fewest questions the case allows, with short plain words. A bad plan has one question too many. A wordy plan has the right count, a 50-word prompt, and a correct option that its length gives away. `prove` passes when every good plan passes the `plan` check and every bad and wordy plan fails it. A wordy plan must fail on its words alone. Run `prove` after you change a check, `quizlint`, or a case.

`prove` costs nothing. It copies `evals/suite` to `evals/.build/oracle-suite` without the judge, so no model is called. The copy keeps every case, fixture, and check file.

`run` and `compare` refuse to start until every subject and the judge have a key. Without that check, multeval would record an unauthenticated session as completed ([multeval#21](https://github.com/krimvp/multeval/issues/21)).

## The gate

`evals/gate.json` holds the quality bar. `fail-under` lists the means that must reach a value: plan passes, skill loads, and the judge score. `fail-over` lists the means that must stay at or below a value. These are word counts, code names, give-aways, filler, tokens, and time. `gate` exits 1 when a subject misses the bar.

The plain values pass the current skill and fail the quizzes of October 2026. Those had prompts of about 34 words, options of about 20, and more than one code name per question. The usage values are a first guess from one attempt. It took about 110 seconds, 380,000 input tokens, and 26,000 output tokens. Tighten them once more runs are kept.

pi on Ollama Cloud reports USD 0, because Ollama Cloud is a subscription. So the gate holds tokens and time, not USD. A `pricing` check with a price table gives an estimated USD for a subject that needs one. See multeval's [measure resources](https://github.com/krimvp/multeval/blob/main/docs/how-to/measure-resources.md) guide.

## Regrade

`regrade` applies today's offline checks to a run that is already made. So a changed rubric or lint scores old raw runs again. The plain check carries today's `quizlint`. The judge carries today's rubric and model, and it reads each case's brief from the run. A run of one case with no judge check gets that case's brief from `evals/suite`. A run of many cases with no judge check gets no judge. One check list cannot hold a brief per case.

Regrade both runs before you `diff` them. A check that only one run has makes the two runs not comparable.

## Subjects

- `run-ollama.json`, the default, is pi on `ollamacloud/glm-5.3`. It needs only an Ollama Cloud key.
- `run.json` is Claude Code on Sonnet 5.5. It needs `CLAUDE_CODE_OAUTH_TOKEN` (from `claude setup-token`) or `ANTHROPIC_API_KEY`. Claude Code cannot be pointed at Ollama Cloud yet ([multeval#25](https://github.com/krimvp/multeval/issues/25)).
- `run-harnesses.json` is Claude Code and Codex. Codex needs `OPENAI_API_KEY`. The judge reads the same key, so set `OPENAI_BASE_URL` to the judge's endpoint too.
- Droid is not a subject yet. multeval's Droid adapter runs on the host and takes no case environment, and each case here builds its git fixture in Docker ([multeval#22](https://github.com/krimvp/multeval/issues/22)).

The paid specs set no `budget_usd`. The judge reports tokens but no USD, and multeval stops paid work under a budget once a cost is unknown.

## Results

Runs land in `evals/runs/`, which git ignores. A run worth keeping goes through `keep`. Per attempt, it keeps the quiz plan, the five grades, the trajectory, and the status. Per run, it writes `summary.json` with the means of each subject from `multeval report`. It also writes a `README.md` table. Add a Findings section to that README by hand.

`keep` then writes `evals/QUALITY.md` again: one row per kept run and subject, oldest first. It shows the plugin version and commit, plan passes, skill loads, the judge score, the plain metrics, and usage.

Runs kept before the grades moved into multeval have no plain, judge, or usage grades. `quality` writes their `summary.json` from their kept files. Plain comes from their `quiz.json` with today's `quizlint`. Usage comes from their `attempt.json`, which is what the usage grader reads. The judge score is from the old `judge.py` and an older rubric. A value the files do not hold stays a dash.

## Keys

`evals/eval` loads `evals/.env`, which git ignores. It is a shell file, so it can read a key from another private file instead of copying it:

```bash
OLLAMA_API_KEY="$(sed -n 's/^OLLAMA_API_KEY=//p' "$HOME/workspace/aigent/.env")"
```

The judge calls an OpenAI-compatible endpoint. When `OPENAI_API_KEY` is unset, `evals/eval` sets it to `OLLAMA_API_KEY` and points `OPENAI_BASE_URL` at `https://ollama.com/v1`.

## Cases

`cases.json` is the source. `evals/build` turns it into `suite/` and `oracle/`. Never edit those by hand. A case names its repo and the `base` and `head` of the change. It also names the altitudes that fit, the question range, the target, and the incidental parts. The judge's brief is written from the target, the altitudes, the incidental parts, and the range.

To add a case, add a row and run `evals/eval build`, then `evals/eval prove`. The aigent cases read the aigent repo from `../aigent`. Pass `--repo aigent=PATH` to `evals/build` when it lives elsewhere. When the repo is missing, `build` keeps the committed fixture and writes only the checks and `case.json`. It fails when the fixture is missing too.

## multeval

`requirements.txt` follows multeval `main`. `requirements.lock.txt` pins the commit the evals last ran on. `evals/eval lock` moves the pin to the current `main`. `MULTEVAL_SRC=PATH` uses a local multeval checkout instead of the pin.
