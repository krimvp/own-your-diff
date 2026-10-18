---
name: own-your-diff
description: "Before any push or PR: explain the unpushed change in an HTML walkthrough, then quiz the author until they show they own the design. The pre-push hook blocks commits without a passed quiz. Use when pushing, opening a PR, or when a push was blocked by own-your-diff."
---

# Own your diff

The author pushes only work they can explain. You write a walkthrough, the author reads it, an examiner quizzes them, and a pass unlocks the push. The quiz checks that the author can reason about the change at the right **altitude**. It is not a memory test of the walkthrough.

Tools are in `scripts/`. Run each with no arguments for its commands.

- `quizgate` is the gate. The pre-push hook calls `quizgate check`. `quizgate install` opts a repo in. Commit the `.own-your-diff` file it writes, and the plugin's session hook installs the git hook in every clone that has it.
- `snippet` renders real git content as editor-style HTML blocks.
- `plainlint` checks the walkthrough for leftover placeholders, and notes long sentences and paragraphs.
- `quizlint` checks a quiz file against [`references/quiz-file.md`](references/quiz-file.md).
- `quizstats` counts questions and pass rates by category and kind across quiz files.

## Steps

Asked for the quiz plan only, as an eval does? Do steps 1 and 2, skip the walkthrough, and write the plan of step 4 for a human examinee to the path you were given. Stop when `quizlint --plan` passes on it. Ask nothing.

### 1. Scope

Run `quizgate pending`. That is the scope: the commits a push would send that have no passed quiz. Diff them with `git diff $(quizgate base) HEAD`. Read the commit messages, and the task that produced the change if this session or its transcript has it.

Done when you can name the **target** of the task: the one thing the work set out to change.

### 2. Pick the altitude

The target sets the altitude. A change can carry both kinds.

- **Design altitude.** The default. The change introduces or reshapes an abstraction, a module boundary, a data shape, a protocol, a dependency, or how components talk. Cover the problem it solves, the shape chosen, how it fits the existing architecture, the alternatives and why they lost, the costs it adds, and what it makes easy or hard next.
- **Mechanism altitude.** The target is one mechanism, for example LLM prompt-cache hits, retry and backoff, stream backpressure, or a bug's root cause. Go through that mechanism's ins and outs: inputs, state, invariants, what invalidates or breaks it, the root cause, why the fix works, and how it was measured. Stay above function names and signatures.
- **Incidental.** Helpers, renames, plumbing, version bumps, and test scaffolding that serve the target. Give each one line and no question.
- **Trivial.** The whole change is a typo, formatting, a version bump, or a one-line config change. Write a short walkthrough. The quiz usually has no questions.

Done when every hunk in the diff belongs to the target or to the incidental list.

### 3. Write the walkthrough

Copy `assets/explainer.html` to `$(quizgate dir)/<branch>-<short-sha>.html`. Write it as a short course: each lesson builds on the one before, and each one teaches a single idea. Fill in the template's lessons in order. Delete a lesson that has nothing to say, and renumber the rest.

Write plain English, in the spirit of ASD-STE100 and Orwell's rules. The reader is learning the change, so teach it directly. These are guidelines. Keep a longer sentence when joining two ideas makes them clearer.

- Open each lesson with one sentence that says what it teaches. Then give a concrete example, then the general rule, then the code.
- Prefer short sentences with one idea each, about 20 words or fewer.
- Use the active voice and name who does what: "the grader reads the file", not "the file is read".
- Choose the short, common word. Use one word for one thing on every line of the page.
- Define a new term in a plain sentence the first time it appears.
- Cut every word that does no work.

- Put code on the page only through `snippet` directives, each on its own line. Then run `snippet expand <file>`. Expanding again refreshes every block from git.
  - `<!-- snippet tree -->` shows the changed files.
  - `<!-- snippet diff PATH [HUNK...] -->` shows a diff, all hunks or the 1-based hunks named.
  - `<!-- snippet file PATH START END [REV] -->` shows file lines in an editor block.
- Show diffs where the target lives, and only the hunks that carry it. Use `file` blocks for code the reader needs whole, such as a new type or the core function. Incidental files appear only in the tree and in the "Also in this change" list.
- Draw the design as an inline SVG with the template's `new`, `box`, `arrow`, and `lbl` classes. A diagram shows the real components and marks what is new.
- Keep the quiz off the page.

Run `plainlint <file>`. It fails on a template placeholder left on the page. It also prints a note for each long sentence and long paragraph. Reread each note, and shorten the prose unless the longer form is clearer.

Open the file with `quizgate open <file>` and give the author its path.

Done when the page renders with every directive expanded, `plainlint` passes and you reread its notes, and the author confirms they read it.

### 4. Quiz

Pick the examinee:

- **Human** whenever a human is in the session to answer. This is the default.
- **Agent** only on an unattended run: a headless session, an autonomous or autopilot playbook, or the human said they are away. Follow [`references/agent-mode.md`](references/agent-mode.md) instead of the rest of this step. A slow human, or a human who declines the quiz, is not an unattended run.

Write between 0 and 10 questions. Ask one only where it makes sense: each question tests a point at the target's altitude that the author must own to stand behind the push. Incidental items get none. Most design changes need 3 to 6. A trivial change usually needs 0.

For each question, list the key points a correct answer must cover. Every key point sits at the target's altitude. At design altitude, a point about one tool's setup step, a flag, or a config value is a mechanism detail, so it stays out of the rubric. Keep the rubric to yourself until the quiz ends.

Ask **transfer** questions. A transfer question makes the author apply the design to a case the walkthrough did not spell out:

- Design. `rationale`: "Why this abstraction over <the rejected alternative>?" `failure`: "What breaks if <assumption> stops holding?" `extension`: "A new <requirement> arrives. Where does it go, and what changes?" `boundary`: "What does this boundary protect the rest of the system from?"
- Mechanism. `flow`: "Walk a request through <mechanism>. Where can it miss or fail?" `invalidation`: "What invalidates <cache or state>?" `measurement`: "Why did <the number> move, and what would move it back?" `failure` fits here too.

Give each question the one category it tests. Spread a quiz across categories rather than asking the same kind of question twice.

Mix three kinds:

- **Single-select.** One correct option among 2 to 4. Lead the quiz with these. They frame a point quickly.
- **Multi-select.** 3 or 4 options, any subset of them correct, for "which of these hold or break" cases. It passes only on the exact set.
- **Free-form.** The author answers in their own words. Use it where the reasoning is the point.

End the quiz with a multi-select or a free-form question that applies several points to one new case. That is where the pieces come together. Every wrong option is a plausible misreading of the change, never filler. Put options in random order and mark none of them.

Write the questions as a plan to `$(quizgate dir)/<branch>-<short-sha>.quiz.json`, in the shape of [`references/quiz-file.md`](references/quiz-file.md). Run `quizlint --plan` on it and fix what it reports before the first question.

Ask one question at a time and wait for the answer. Use the harness's structured-question tool when it has one: `AskUserQuestion` in Claude Code, `AskUser` in Droid, `request_user_input` in Codex where it is enabled. Where the tool has no multi-select, or there is no tool, ask in chat with lettered options and say whether to pick one or several. Never answer for the author.

After each select question, say which options were right and why in one or two sentences, so a wrong pick turns into a gotcha the author remembers. Grade each answer against its key points:

- **Pass.** It covers the core point with sound reasoning, or picks the right options. Wording and depth beyond the point do not matter.
- **Vague.** Ask one follow-up probe on the missing point.
- **Wrong or still vague.** Explain the gap in two or three sentences. Then ask a new question that targets the same point from another angle.

A probe or retry stays at the altitude of the question it follows. It tests the same key point in a new case, never a finer detail of how that point is implemented. At design altitude, "the gate keys on diff content, not commits" is the point. How a partial squash hashes is a mechanism detail, so it is out of bounds.

Done when every question is passed, or a point fails three times. With no questions, done when the author confirms they read the walkthrough. On three failures, stop and record nothing. Tell the author which part to reread or go through with you. If the walkthrough was the problem, say the change may be too large or unclear, and suggest splitting it.

### 5. Record

As the quiz runs, add each answer to its question in the quiz file as an attempt: the author's words or picks verbatim, your verdict, and what you told them. On a full pass, set `outcome` to `passed` and run `quizlint` on the file until it passes. Then run `quizgate record --by human`, or `--by agent` after agent mode.

Done when `quizgate pending` prints nothing. Push only if you were asked to push.

## Rules

- A pass belongs to the examinee who earned it in this session. Run `quizgate record` only after that pass.
- Push with the hook active. `--no-verify` is the human's call, never yours.
- A blocked push routes back to step 1 for the commits the hook names. The ledger keys passes on `git patch-id`, so rewording, rebasing, or squashing quizzed commits needs no new quiz. New content does.
- For a PR, draw the body from the walkthrough's Why, Scope, and Tradeoffs. The walkthrough and quiz file stay out of the tree.
