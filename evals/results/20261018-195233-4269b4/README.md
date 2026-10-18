# Run 20261018-195233-4269b4

Subjects: pi-glm-base (pi 1.3.0, ollamacloud/glm-5.3), pi-glm (pi 1.3.0, ollamacloud/glm-5.3).

| case | subject | plan | skill loaded | questions | altitude | kinds | judge | judge missed |
|---|---|---|---|---|---|---|---|---|
| aigent-invariant-judge | pi-glm | True | True | 8 | design | single, single, single, multi, free, free, single, multi | - | - |
| aigent-invariant-judge | pi-glm | True | True | 7 | design | single, single, multi, single, multi, free, multi | - | - |
| aigent-scenario-runs | pi-glm | True | True | 9 | design | single, single, multi, single, free, multi, free, single, free | - | - |
| aigent-scenario-runs | pi-glm | True | True | 10 | design | single, single, multi, single, multi, single, free, single, multi, free | - | - |
| aigent-secret-split | pi-glm | False | True | 7 | mechanism | single, single, free, multi, single, free, multi | - | - |
| aigent-secret-split | pi-glm | True | True | 5 | mechanism | single, single, multi, single, free | - | - |
| aigent-short-secret | pi-glm | False | True | 4 | mechanism | single, multi, single, free | - | - |
| aigent-short-secret | pi-glm | False | True | 4 | mechanism | single, multi, single, free | - | - |
| oyd-docs-install | pi-glm | False | True | 5 | design | single, single, single, free, multi | - | - |
| oyd-docs-install | pi-glm | False | True | 6 | design | single, single, single, multi, free, multi | - | - |
| oyd-marker-opt-in | pi-glm | True | True | 4 | design | single, single, multi, free | - | - |
| oyd-marker-opt-in | pi-glm | True | True | 4 | design | single, single, multi, free | - | - |
| oyd-plugin-packaging | pi-glm | True | True | 5 | design | single, single, single, free, multi | - | - |
| oyd-plugin-packaging | pi-glm | True | True | 7 | design | single, single, single, single, multi, free, multi | - | - |
| oyd-release-bump | pi-glm | True | True | 0 | trivial |  | - | - |
| oyd-release-bump | pi-glm | True | True | 0 | trivial |  | - | - |
| oyd-stale-hookspath | pi-glm | True | True | 4 | mechanism | single, single, multi, free | - | - |
| oyd-stale-hookspath | pi-glm | True | True | 4 | mechanism | single, multi, free, multi | - | - |

## Questions

```
18 quizzes, 93 questions, questions per quiz: 0x2, 4x6, 5x3, 6x1, 7x3, 8x1, 9x1, 10x1
outcomes: plan 18

                       questions  answered  first pass  passed  retries
category boundary             16         0           -       0        0
category extension            14         0           -       0        0
category failure              25         0           -       0        0
category flow                 10         0           -       0        0
category invalidation          7         0           -       0        0
category measurement           5         0           -       0        0
category rationale            16         0           -       0        0
kind free                     21         0           -       0        0
kind multi                    26         0           -       0        0
kind single                   46         0           -       0        0
relevance None                93         0           -       0        0
```
## Findings

Stopped after the branch side, 16 of 18 attempts, at a88532f: "count the points to own" and "docs-only is trivial". `main`'s side did not run. The first full run, 20261018-180310-adb89b, is `main`'s skill.

- **The count followed the size, but upward.** Big changes went from 5 questions to 7 to 10. The 23-line fix stayed at 4 in both trials.
- **The docs case still got 5 and 6 questions.** The agent applied the rule as written: the AGENTS.md in that commit states contributor rules, and the rule made a doc's rules the target. So it asked about bumping the version and running the selftest. The next commit makes contributor steps incidental.
