---
name: own-your-diff
description: "Before any push or PR: explain the unpushed change in an HTML walkthrough, then quiz the author until they show they own the design. The pre-push hook blocks commits without a passed quiz. Use when pushing, opening a PR, or when a push was blocked by own-your-diff."
---

# Own your diff

The author pushes only work they can explain. You write a walkthrough, the author reads it, an examiner quizzes them, and a pass unlocks the push. The quiz checks that the author can reason about the change at the right **altitude**. It is not a memory test of the walkthrough.

Tools are in `scripts/`. Run each with no arguments for its commands.

- `quizgate` is the gate. The pre-push hook calls `quizgate check`. In a fresh clone, run `quizgate install` once.
- `snippet` renders real git content as editor-style HTML blocks.
- `selftest` runs both through real `git push`. Run it after you change either one.

## Steps

### 1. Scope

Run `quizgate pending`. That is the scope: the commits a push would send that have no passed quiz. Diff them with `git diff $(quizgate base) HEAD`. Read the commit messages, and the task that produced the change if this session or its transcript has it.

Done when you can name the **target** of the task: the one thing the work set out to change.

### 2. Pick the altitude

The target sets the altitude. A change can carry both kinds.

- **Design altitude.** The default. The change introduces or reshapes an abstraction, a module boundary, a data shape, a protocol, a dependency, or how components talk. Cover the problem it solves, the shape chosen, how it fits the existing architecture, the alternatives and why they lost, the costs it adds, and what it makes easy or hard next.
- **Mechanism altitude.** The target is one mechanism, for example LLM prompt-cache hits, retry and backoff, stream backpressure, or a bug's root cause. Go through that mechanism's ins and outs: inputs, state, invariants, what invalidates or breaks it, the root cause, why the fix works, and how it was measured. Stay above function names and signatures.
- **Incidental.** Helpers, renames, plumbing, and test scaffolding that serve the target. Give each one line and no question.
- **Trivial.** The whole change is a typo, formatting, a version bump, or a one-line config change. Write a short walkthrough and ask one question about intent and impact.

Done when every hunk in the diff belongs to the target or to the incidental list.

### 3. Write the walkthrough

Copy `assets/explainer.html` to `$(quizgate dir)/<branch>-<short-sha>.html`. Write it as a short course: each lesson builds on the one before, and each one teaches a single idea. Fill in the template's lessons in order. Delete a lesson that has nothing to say, and renumber the rest.

- Put code on the page only through `snippet` directives, each on its own line. Then run `snippet expand <file>`. Expanding again refreshes every block from git.
  - `<!-- snippet tree -->` shows the changed files.
  - `<!-- snippet diff PATH [HUNK...] -->` shows a diff, all hunks or the 1-based hunks named.
  - `<!-- snippet file PATH START END [REV] -->` shows file lines in an editor block.
- Show diffs where the target lives, and only the hunks that carry it. Use `file` blocks for code the reader needs whole, such as a new type or the core function. Incidental files appear only in the tree and in the "Also in this change" list.
- Draw the design as an inline SVG with the template's `new`, `box`, `arrow`, and `lbl` classes. A diagram shows the real components and marks what is new.
- Keep the quiz off the page.

Open the file with `quizgate open <file>` and give the author its path.

Done when the page renders with every directive expanded, and the author confirms they read it.

### 4. Quiz

Pick the examinee:

- **Human** whenever a human is in the session to answer. This is the default.
- **Agent** only on an unattended run: a headless session, an autonomous or autopilot playbook, or the human said they are away. Follow [`references/agent-mode.md`](references/agent-mode.md) instead of the rest of this step. A slow human, or a human who declines the quiz, is not an unattended run.

Write 3 to 5 questions for design or mechanism altitude, or 1 for trivial. For each question, list 2 to 4 key points a correct answer must cover. Keep this rubric to yourself until the quiz ends.

Ask **transfer** questions. A transfer question makes the author apply the design to a case the walkthrough did not spell out:

- Design: "Why this abstraction over <the rejected alternative>?" "What breaks if <assumption> stops holding?" "A new <requirement> arrives. Where does it go, and what changes?" "What does this boundary protect the rest of the system from?"
- Mechanism: "Walk a request through <mechanism>. Where can it miss or fail?" "What invalidates <cache or state>?" "Why did <the number> move, and what would move it back?"

Ask one question at a time in plain chat, open-ended. Wait for the author's answer in their own words. Never answer for them, and never offer options to pick from.

Grade each answer against its key points:

- **Pass.** It covers the core point with sound reasoning. Wording and depth beyond the point do not matter.
- **Vague.** Ask one follow-up probe on the missing point.
- **Wrong or still vague.** Explain the gap in two or three sentences. Then ask a new question that targets the same point from another angle.

Done when every question is passed, or a point fails three times. On three failures, stop and record nothing. Tell the author which part to reread or go through with you. If the walkthrough was the problem, say the change may be too large or unclear, and suggest splitting it.

### 5. Record

On a full pass, write the transcript to `$(quizgate dir)/<branch>-<short-sha>.quiz.md`. Include each question, the answers verbatim, your verdicts, and the rubric. Then run `quizgate record --by human`, or `--by agent` after agent mode.

Done when `quizgate pending` prints nothing. Push only if you were asked to push.

## Rules

- A pass belongs to the examinee who earned it in this session. Run `quizgate record` only after that pass.
- Push with the hook active. `--no-verify` is the human's call, never yours.
- A blocked push routes back to step 1 for the commits the hook names. The ledger keys passes on `git patch-id`, so rewording, rebasing, or squashing quizzed commits needs no new quiz. New content does.
- For a PR, draw the body from the walkthrough's Why, Scope, and Tradeoffs. The walkthrough and transcript stay out of the tree.
