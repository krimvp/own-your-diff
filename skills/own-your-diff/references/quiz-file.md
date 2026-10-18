# The quiz file

One JSON file per quiz, `$(quizgate dir)/<branch>-<short-sha>.quiz.json`. You write it as a **plan** before the first question, and you add each attempt and the outcome as the quiz runs. `scripts/quizlint --plan FILE` checks a plan. `scripts/quizlint FILE` checks a finished quiz. Evals and stats read this file, and a UI can render it, so keep to this shape.

```json
{
  "version": 1,
  "branch": "feat/opt-in-marker",
  "base": "42c2cb8",
  "head": "0389727",
  "target": "Repos opt into the gate with a tracked marker instead of core.hooksPath.",
  "altitude": "design",
  "incidental": ["usage text of quizgate"],
  "examinee": "human",
  "questions": [
    {
      "id": "q1",
      "kind": "single",
      "category": "rationale",
      "prompt": "Why does the hook run quizgate from ~/.local/bin and not from the plugin's install directory?",
      "options": [
        { "label": "The install directory holds the version and moves on update", "correct": true },
        { "label": "Git refuses hooks outside the repo", "correct": false },
        { "label": "The plugin directory is read-only", "correct": false }
      ],
      "key_points": ["the cache path changes on every update"],
      "attempts": [
        { "answer": ["The install directory holds the version and moves on update"], "verdict": "pass" }
      ]
    }
  ],
  "outcome": "passed"
}
```

- **Top level.** `target` is the one thing the change set out to do. `altitude` is `design`, `mechanism`, or `trivial`. `incidental` lists what gets no question. `examinee` is `human` or `agent`. `questions` holds 0 to 10 questions. `outcome` is `passed` or `failed`, and a plan has none. Agent mode adds `findings`, one object per finding with its round, evidence, and fix.
- **Question.** `kind` is `single`, `multi`, or `free`. A `single` question has 2 to 4 options with exactly one correct. A `multi` question has 3 or 4 options with at least one correct. A `free` question has no options. `key_points` is the rubric. `attempts` stays empty in a plan.
- **Category.** Each question has one. Design questions are `rationale` (why this over the alternative), `failure` (what breaks when an assumption stops holding), `extension` (where a new requirement goes), or `boundary` (what a boundary protects). Mechanism questions are `flow` (walk the mechanism, where it can fail), `invalidation` (what invalidates the state), `measurement` (why the number moved), or `failure`.
- **Attempt.** One per answer, in order. A probe or a retry adds an attempt with its own `prompt`, and `kind` and `options` when they differ from the question's. `answer` is the author's words verbatim, or the list of labels they picked. `verdict` is `pass`, `vague`, or `wrong`. `feedback` is what you told them. Agent mode adds `round`.
