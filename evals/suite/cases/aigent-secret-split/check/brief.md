# Case brief

This brief is for the judge of the quiz plan. The agent that wrote the plan never saw it.

## The target of the change

The text stream holds back the last (longest secret - 1) characters across the whole assistant message, so a secret split across text deltas or text blocks never reaches a listener whole. It flushes at message_end and never cuts a surrogate pair.

## Altitudes that fit

- mechanism: the inputs, state, invariants, and failure modes of the one mechanism the change targets, above function names and signatures

## Incidental parts

- the test helper names
- the variable names in pi.ts

## Size

The plan holds 2 to 6 questions.

## Reading the criteria

A criterion about every question is met when quiz.json has no questions.
A criterion that starts with "When" is met when its condition does not hold.
