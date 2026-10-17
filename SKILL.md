---
name: own-your-diff
description: "Before any push or PR: explain the unpushed change in an HTML explainer, then quiz the human author until they show they own the design. The pre-push hook blocks commits without a passed quiz. Use when pushing, opening a PR, or when a push was blocked by own-your-diff."
---

# Own your diff

The human pushes only work they can explain. You write the explainer, the human reads it, you quiz them, and a pass unlocks the push. The quiz checks that the author can reason about the change at the right **altitude**. It is not a memory test of the explainer.

The gate is `scripts/quizgate` (run with no arguments for its commands). The pre-push hook calls `quizgate check`. In a fresh clone, run `quizgate install` once.

## Steps

### 1. Scope

Run `quizgate pending`. That is the scope: the commits a push would send that have no passed quiz. Diff them with `git diff $(quizgate base) HEAD`. Read the commit messages, and the task that produced the change if this session or its transcript has it.

Done when you can name the **target** of the task: the one thing the work set out to change.

### 2. Pick the altitude

The target sets the altitude. A change can carry both kinds.

- **Design altitude.** The default. The change introduces or reshapes an abstraction, a module boundary, a data shape, a protocol, a dependency, or how components talk. Cover the problem it solves, the shape chosen, how it fits the existing architecture, the alternatives and why they lost, the costs it adds, and what it makes easy or hard next.
- **Mechanism altitude.** The target is one mechanism, for example LLM prompt-cache hits, retry and backoff, stream backpressure, or a bug's root cause. Go through that mechanism's ins and outs: inputs, state, invariants, what invalidates or breaks it, the root cause, why the fix works, and how it was measured. Stay above function names and signatures.
- **Incidental.** Helpers, renames, plumbing, and test scaffolding that serve the target. Give each one line and no question.
- **Trivial.** The whole change is a typo, formatting, a version bump, or a one-line config change. Write a short explainer and ask one question about intent and impact.

Done when every hunk in the diff belongs to the target or to the incidental list.

### 3. Write the explainer

Copy `assets/explainer.html` to `$(quizgate dir)/<branch>-<short-sha>.html` and fill it in. Use the template's sections in order. Delete any section that has nothing to say. Draw the design as an inline SVG or a `<pre>` box diagram. A diagram must show the real components and the arrows that changed.

Keep the quiz out of the explainer. Open the file with `quizgate open <file>`, give the human its path, and wait until they say they have read it.

Done when the human confirms they read the explainer.

### 4. Quiz

Write 3 to 5 questions for design or mechanism altitude, or 1 for trivial. Keep the rubric to yourself. For each question, list 2 to 4 key points a correct answer must cover. Do not put the rubric in chat or in a file before the quiz ends.

Ask **transfer** questions, which make the author apply the design to something the explainer did not spell out:

- Design: "Why this abstraction over <the rejected alternative>?" "What breaks if <assumption> stops holding?" "A new <requirement> arrives. Where does it go, and what changes?" "What does this boundary protect the rest of the system from?"
- Mechanism: "Walk a request through <mechanism>. Where can it miss or fail?" "What invalidates <cache or state>?" "Why did <the number> move, and what would move it back?"

Ask one question at a time in plain chat, open-ended. Wait for the human's answer in their own words. Never answer for them, and never offer options to pick from.

Grade each answer against its key points:

- **Pass.** It covers the core point with sound reasoning. Wording and depth beyond the point do not matter.
- **Vague.** Ask one follow-up probe on the missing point.
- **Wrong or still vague.** Explain the gap in two or three sentences. Then ask a new question that targets the same point from another angle.

Done when every question is passed, or a point fails three times. On three failures, stop and record nothing. Tell the human which part to reread or reopen with you. If the explanation itself was the problem, say the change may be too large or unclear and suggest splitting it.

### 5. Record

On a full pass, write the transcript to `$(quizgate dir)/<branch>-<short-sha>.quiz.md`. Include each question, the human's answers verbatim, your verdicts, and the rubric. Then run `quizgate record`.

Done when `quizgate pending` prints nothing. Push only if the human asked you to push.

## Rules

- A pass is the human's. Run `quizgate record` only after the human passed this quiz in this session.
- Push with the hook active. `--no-verify` is the human's call, never yours.
- A blocked push routes back to step 1 for the commits the hook names. The ledger keys passes on `git patch-id`, so rewording, rebasing, or squashing quizzed commits needs no new quiz. New content does.
- For a PR, draw the body from the explainer's Why, Scope, and Tradeoffs. The explainer and transcript stay out of the tree.
