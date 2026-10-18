# Run 20261018-180310-adb89b

Subjects: pi-glm (pi 1.3.0, ollamacloud/glm-5.3).

| case | subject | plan | skill loaded | questions | altitude | kinds | judge | judge missed |
|---|---|---|---|---|---|---|---|---|
| aigent-invariant-judge | pi-glm | True | True | 5 | design | single, single, free, multi, free | 1.00 | - |
| aigent-scenario-runs | pi-glm | True | True | 5 | design | single, single, multi, free, free | 1.00 | - |
| aigent-secret-split | pi-glm | True | True | 6 | mechanism | single, single, single, free, free, multi | 1.00 | - |
| aigent-short-secret | pi-glm | False | True | 4 | mechanism | single, single, multi, free | 1.00 | - |
| oyd-docs-install | pi-glm | False | True | 5 | design | single, multi, free, single, multi | 0.80 | 2 |
| oyd-marker-opt-in | pi-glm | True | True | 5 | design | single, single, single, multi, free | 1.00 | - |
| oyd-plugin-packaging | pi-glm | True | True | 5 | design | single, multi, single, multi, free | 1.00 | - |
| oyd-release-bump | pi-glm | True | True | 0 | trivial |  | 1.00 | - |
| oyd-stale-hookspath | pi-glm | True | True | 5 | mechanism | single, single, multi, free, free | 1.00 | - |

## Questions

```
9 quizzes, 40 questions, questions per quiz: 0x1, 4x1, 5x6, 6x1
outcomes: plan 9

                       questions  answered  first pass  passed  retries
category boundary              6         0           -       0        0
category extension             7         0           -       0        0
category failure               9         0           -       0        0
category flow                  6         0           -       0        0
category invalidation          4         0           -       0        0
category measurement           2         0           -       0        0
category rationale             6         0           -       0        0
kind free                     12         0           -       0        0
kind multi                    10         0           -       0        0
kind single                   18         0           -       0        0
```
## Findings

The run used the skill at 478bb73, one trial per case, with the judge on `glm-5.3`.

- **7 of 9 plans fit their case. pi loaded the skill every time.** Every quiz with questions opened on a single-select and ended on a multi-select or free-form question.
- **`oyd-docs-install` failed the plan check.** It is a docs-only change, and it got 5 design questions about the design the README describes, which was quizzed when it was built. The skill has no rule for a change that only documents existing behavior. The judge missed criterion 2, the altitude.
- **`aigent-short-secret` failed the plan check.** A 15-line fix got 4 questions where the case allows 0 to 3. The questions are sound, and the judge gave 1.00, so the range stays: a fix this small should not get four.
- **The count barely moves with the size of the change.** 6 of the 8 quizzes with questions had exactly 5, from a 15-line fix to a 1,955-line change. The skill's "most design changes need 3 to 6" may anchor it. This rests on one trial per case, so it is a guess until a comparison run backs it up.
- **The judge rarely discriminates.** It scored 8 of 9 at 1.00. A deliberately bad plan for `oyd-marker-opt-in` scored 0.00, so it catches gross misses, but subtler problems may pass it.
