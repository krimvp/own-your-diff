# Case brief

This brief is for the judge of the quiz plan. The agent that wrote the plan never saw it.

## The target of the change

A repo opts into the push gate with a tracked .own-your-diff marker. quizgate install writes the pre-push hook into the clone's own hooks directory instead of pointing core.hooksPath at a tracked .githooks dir, and quizgate sync keeps a copy of quizgate on PATH and installs the hook in opted-in clones that lack it.

## Altitudes that fit

- design: the problem the change solves, the shape chosen, the alternatives, and what it makes easy or hard next, above function names and flags

## Incidental parts

- the selftest file moving to the repo root
- the usage text of quizgate
- the wording edits in SKILL.md and agent-mode.md

## Size

The plan holds 2 to 6 questions.

## Reading the criteria

A criterion about every question is met when quiz.json has no questions.
A criterion that starts with "When" is met when its condition does not hold.
