# Run 20261110-052148-ae0e7f

Subjects: pi-glm (pi 1.5.1, ollamacloud/glm-5.3).

| case | subject | trial | plan | skill loaded | questions | altitude | kinds | prompt words | option words | code names | giveaways | fluff | judge | judge missed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aigent-invariant-judge | pi-glm | trial-01 | True | True | 6 | design | single, single, single, multi, free, multi | 24.8 | 14.6 | 0.00 | 0 | 0 | 1.00 | - |
| aigent-scenario-runs | pi-glm | trial-01 | True | True | 8 | design | single, multi, single, free, multi, single, free, multi | 21.9 | 10.5 | 0.00 | 0 | 0 | 1.00 | - |
| aigent-secret-split | pi-glm | trial-01 | True | True | 3 | mechanism | single, free, multi | 26.3 | 11.5 | 0.00 | 0 | 0 | 1.00 | - |
| aigent-short-secret | pi-glm | trial-01 | True | True | 3 | mechanism | single, free, multi | 19.3 | 10.6 | 0.00 | 0 | 0 | 1.00 | - |
| oyd-docs-install | pi-glm | trial-01 | True | True | 0 | trivial |  | 0.0 | 0.0 | 0.00 | 0 | 0 | 1.00 | - |
| oyd-marker-opt-in | pi-glm | trial-01 | True | True | 4 | design | single, single, multi, free | 24.2 | 12.8 | 0.00 | 0 | 0 | 1.00 | - |
| oyd-plugin-packaging | pi-glm | trial-01 | True | True | 5 | design | single, free, single, free, multi | 21.2 | 10.2 | 0.00 | 0 | 0 | 1.00 | - |
| oyd-release-bump | pi-glm | trial-01 | True | True | 0 | trivial |  | 0.0 | 0.0 | 0.00 | 0 | 0 | 1.00 | - |
| oyd-stale-hookspath | pi-glm | trial-01 | True | True | 3 | mechanism | single, free, multi | 25.3 | 12.8 | 0.67 | 0 | 0 | 1.00 | - |

## Questions

```
9 quizzes, 32 questions, questions per quiz: 0x2, 3x3, 4x1, 5x1, 6x1, 8x1
outcomes: plan 9

                       questions  answered  first pass  passed  retries
category boundary              6         0           -       0        0
category extension             5         0           -       0        0
category failure               9         0           -       0        0
category flow                  2         0           -       0        0
category invalidation          2         0           -       0        0
category rationale             8         0           -       0        0
kind free                      9         0           -       0        0
kind multi                    10         0           -       0        0
kind single                   13         0           -       0        0
relevance core                18         0           -       0        0
relevance important           14         0           -       0        0
```

## Findings

The skill at 89ddff1 (0.7.0), after the rule that tests each point: would a reviewer stop the push without it? One trial per case, on multeval 7d9d76e.

- **Every plan passed, and the judge met every criterion on all nine.** The run passes the gate.
- **Large changes got fewer questions.** `aigent-scenario-runs` got 8, where it got 10 before. `oyd-marker-opt-in` got 4, where it got 6 and 8. The mean went from 4.4 to 3.6.
- **Both trivial cases got 0 questions, and each small fix got 3.**
- **The word means in this row count a quiz with no questions as 0.** Earlier rows left those quizzes out, so compare with care: over the seven quizzes with questions, prompts have 23.3 words and options 11.9.
- **One trial per case is a small sample.** Run `evals/eval compare` for a firm number.
