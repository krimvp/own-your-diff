# Run 20261018-202951-aa03df

Subjects: pi-glm (pi 1.3.0, ollamacloud/glm-5.3).

| case | subject | plan | skill loaded | questions | altitude | kinds | judge | judge missed |
|---|---|---|---|---|---|---|---|---|
| aigent-scenario-runs | pi-glm | True | True | 9 | design | single, multi, single, free, free, free, single, free, multi | 0.86 | 5 |
| aigent-secret-split | pi-glm | True | True | 5 | mechanism | single, single, single, free, multi | 1.00 | - |
| aigent-short-secret | pi-glm | False | True | 4 | mechanism | single, single, multi, free | 1.00 | - |
| oyd-docs-install | pi-glm | False | True | 2 | design | single, multi | 0.67 | 1, 2 |
| oyd-release-bump | pi-glm | True | True | 0 | trivial |  | 1.00 | - |

## Questions

```
5 quizzes, 20 questions, questions per quiz: 0x1, 2x1, 4x1, 5x1, 9x1
outcomes: plan 5

                       questions  answered  first pass  passed  retries
category boundary              3         0           -       0        0
category extension             2         0           -       0        0
category failure               6         0           -       0        0
category flow                  3         0           -       0        0
category invalidation          2         0           -       0        0
category measurement           1         0           -       0        0
category rationale             3         0           -       0        0
kind free                      6         0           -       0        0
kind multi                     5         0           -       0        0
kind single                    9         0           -       0        0
relevance core                 9         0           -       0        0
relevance important           11         0           -       0        0
```
## Findings

Quick run of five targeted cases, one trial each. The skill counts only `core` and `important` points, treats contributor steps as incidental, and asks outside in.

- **The docs-only case went from 5 and 6 questions to 2,** both `core`, about the rules the new AGENTS.md sets. That is still one over its 0-to-1 range.
- **The 23-line fix still got 4 questions,** one over its 0-to-3 range.
- **The 80-line fix fit, with 5 questions. The big change kept 9. The version bump kept 0.**
- **No question was rated `useful`. Every quiz opened on `core` questions.**
