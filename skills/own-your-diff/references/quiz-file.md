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
      "relevance": "core",
      "prompt": "Why does the hook run quizgate from ~/.local/bin and not from the plugin's install directory?",
      "options": [
        { "label": "The install directory changes with each plugin update", "correct": true },
        { "label": "Git refuses to run a hook from outside the repo", "correct": false },
        { "label": "The hook cannot read files in the plugin directory", "correct": false }
      ],
      "key_points": ["the cache path changes on every update"],
      "attempts": [
        { "answer": ["The install directory changes with each plugin update"], "verdict": "pass" }
      ]
    }
  ],
  "outcome": "passed"
}
```

- **Top level.** `target` is the one thing the change set out to do. `altitude` is `design`, `mechanism`, or `trivial`. `incidental` lists what gets no question. `examinee` is `human` or `agent`. `questions` holds 0 to 10 questions. `outcome` is `passed` or `failed`, and a plan has none. Agent mode adds `findings`, one object per finding with its round, evidence, and fix.
- **Question.** `relevance` is `core`, `important`, or `useful`, and the questions run from most to least relevant, except the last. `kind` is `single`, `multi`, or `free`. A `single` question has 2 to 4 options with exactly one correct. A `multi` question has 3 or 4 options with at least one correct. A `free` question has no options. `key_points` is the rubric. `attempts` stays empty in a plan. A `useful` question appears only when the quiz has no `core` or `important` question.
- **Words.** Ask at a high level, in plain short words. `quizlint` checks each question in a plan and in a finished quiz.
  - A prompt has 40 words or fewer. Ask one thing in one or two short sentences.
  - An option has 20 words or fewer. A key point has 25 words or fewer. A question has 4 key points or fewer.
  - The correct option of a `single` question is not much longer than the wrong ones. Make the options about the same length.
  - A word from the lists in `plain-english.md` is a note. So is a sentence of more than 20 words in a prompt.
  - A code name in a prompt or option is a note. Code names are function, file, and flag names. Say what the thing does instead. Keep the name only when the question is about it.
  - `quizlint --json` prints the problems, the notes, and the word counts as one JSON object.
- **Category.** Each question has one. Design questions are `rationale` (why this over the alternative), `failure` (what breaks when an assumption stops holding), `extension` (where a new requirement goes), or `boundary` (what a boundary protects). Mechanism questions are `flow` (walk the mechanism, where it can fail), `invalidation` (what invalidates the state), `measurement` (why the number moved), or `failure`.
- **Attempt.** One per answer, in order. A probe or a retry adds an attempt with its own `prompt`, and `kind` and `options` when they differ from the question's. `answer` is the author's words verbatim, or the list of labels they picked. `verdict` is `pass`, `vague`, or `wrong`. `feedback` is what you told them. Agent mode adds `round`.
