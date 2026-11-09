# Case brief

This brief is for the judge of the quiz plan. The agent that wrote the plan never saw it.

## The target of the change

check(run) judges a run from its log alone: five engine invariants that every trial must keep, where one failure is a bug, and nine model behaviors measured as rates that skip when their precondition never happened. Cost is reported and never judged.

## Altitudes that fit

- design: the problem the change solves, the shape chosen, the alternatives, and what it makes easy or hard next, above function names and flags

## Incidental parts

- the names of individual checks
- the TypeScript types of the case tables
- the evidence strings

## Size

The plan holds 3 to 8 questions.

## Reading the criteria

A criterion about every question is met when quiz.json has no questions.
A criterion that starts with "When" is met when its condition does not hold.
