# Agent mode

On an unattended run, the authoring agent is the examinee. Asking yourself questions proves nothing, so two fresh subagents take the examiner's seat. Neither one has seen your context. The quiz now works as **verification**: it catches places where what you say you built differs from what the diff does, and design gaps that only show up when you apply the design to a new case.

Spawn each one fresh, with none of your context. Under pstack, spawn them as `poteto-agent` (see the Subagents and Harness sections of `poteto-mode`). Use a model family different from yours when one is available. Pass file paths, not summaries.

## 1. Examine

Give a fresh **examiner** subagent the range (`$(quizgate base)..HEAD`), the task statement, the walkthrough path, and this skill's `SKILL.md`. Its brief:

- Read the diff in full yourself. Do not trust the walkthrough.
- Check every factual claim in the walkthrough against the diff. List each claim the diff contradicts or does not support, with `path:line` evidence.
- Write 0 to 10 free-form transfer questions per step 4 of `SKILL.md`. Free-form only: a guessed pick proves nothing about an agent's understanding. Return the questions and the claim list. Keep your rubric to yourself.

Done when the examiner has returned its questions and its claim list.

## 2. Answer

Write `$(quizgate dir)/<branch>-<short-sha>.answers.md` with one answer per question. Answer from your understanding of the design, as the author. A question you cannot answer without new digging is a finding. Say so in the answer.

## 3. Grade

Give a fresh **grader** subagent the range, the questions, and your answers file. Its brief:

- Read the diff in full yourself.
- Grade each answer against what the code does, not against how plausible the answer sounds: pass, vague, or wrong.
- For every answer that is not a pass, name the gap with `path:line` evidence.

Done when every answer has a grade with evidence.

## 4. Resolve

Every contradicted claim and every answer that is not a pass is a **finding**. Fix each one at its source. If the code is wrong, fix the code. If the code is right and your understanding was wrong, fix the walkthrough. Commit the fixes, run `snippet expand` again, and start a new round from step 1 with a fresh examiner and fresh questions.

Done when a round has no findings. After three rounds that still have findings, stop. Record nothing, do not push, and report the open findings to the human.

## 5. Record

Write the transcript to `$(quizgate dir)/<branch>-<short-sha>.quiz.md`. Include every round's questions, answers, grades, and findings with their fixes. Then run `quizgate record --by agent`.

The ledger keeps `agent` in the pass, so a human can later see which pushes no human was quizzed on. The walkthrough stays in `$(quizgate dir)` for the human to read when they are back.
