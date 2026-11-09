# Case brief

This brief is for the judge of the quiz plan. The agent that wrote the plan never saw it.

## The target of the change

runScenario refuses a secret or model key shorter than 8 characters as a scenario problem, because the scrub rewrites every occurrence of a raw secret, JSON keys included, and a 1-character key broke the result directory after model calls were spent.

## Altitudes that fit

- mechanism: the inputs, state, invariants, and failure modes of the one mechanism the change targets, above function names and signatures
- design: the problem the change solves, the shape chosen, the alternatives, and what it makes easy or hard next, above function names and flags
- trivial: the intent and impact of the change, if anything

## Incidental parts

- the design doc wording
- the test expectations

## Size

The plan holds 0 to 3 questions.

## Reading the criteria

A criterion about every question is met when quiz.json has no questions.
A criterion that starts with "When" is met when its condition does not hold.
