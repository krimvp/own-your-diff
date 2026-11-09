# Quiz quality over time

One row per kept run and subject, oldest first. `evals/eval keep` writes it from each run's `summary.json`. Rates are the share of attempts, and the other numbers are means over attempts.

Plain counts words in the plan's prompts and options, code names per question, and give-away options and filler words per quiz. Lower is better. Usage is per attempt.

| run | date | version | commit | subject | attempts | plan pass | skill loaded | judge | questions | prompt words | prompt max | option words | option max | code names | giveaways | fluff | duration s | input tokens | output tokens |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 20261018-180310-adb89b | 2026-10-18 | - | - | pi-glm | 9 | 0.78 | 1.00 | 0.98* | 4.4 | 33.9 | 48.1 | 21.4 | 42.9 | 1.70 | 1.33 | 7.00 | 297 | 238311 | 19517 |
| 20261018-195233-4269b4 | 2026-10-18 | - | - | pi-glm | 18 | 0.72 | 1.00 | - | 5.2 | 33.8 | 49.4 | 19.8 | 37.6 | 1.77 | 2.06 | 8.67 | 301 | 261862 | 24153 |
| 20261018-202951-aa03df | 2026-10-18 | - | - | pi-glm | 5 | 0.60 | 1.00 | 0.91* | 4.0 | 34.3 | 48.5 | 20.0 | 46.2 | 1.33 | 1.80 | 4.40 | 451 | 323004 | 22609 |

Runs marked * in the judge column were kept before the grades moved into multeval. Their judge was evals/judge.py, with a rubric that lacked the code-closed and plain-English criteria. Their plain numbers come from their quiz.json with today's quizlint. Their usage comes from the kept attempt, as multeval's usage grader reads it.

A commit with + was kept from a tree with changes to the skill or the suite.
