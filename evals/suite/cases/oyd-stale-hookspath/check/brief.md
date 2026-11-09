# Case brief

This brief is for the judge of the quiz plan. The agent that wrote the plan never saw it.

## The target of the change

A clone whose core.hooksPath names a directory that no longer exists gets it unset at session start, so the hook is installed again. When core.hooksPath names a real directory, such as husky's, install writes nothing there and prints the line to add.

## Altitudes that fit

- mechanism: the inputs, state, invariants, and failure modes of the one mechanism the change targets, above function names and signatures
- design: the problem the change solves, the shape chosen, the alternatives, and what it makes easy or hard next, above function names and flags

## Incidental parts

- the selftest cases
- the realpath flag used

## Size

The plan holds 1 to 5 questions.

## Reading the criteria

A criterion about every question is met when quiz.json has no questions.
A criterion that starts with "When" is met when its condition does not hold.
