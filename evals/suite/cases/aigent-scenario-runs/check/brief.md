# Case brief

This brief is for the judge of the quiz plan. The agent that wrote the plan never saw it.

## The target of the change

Scenarios become data files run by one runner that writes each run as a result directory, a check(run) judge separates engine invariants from model behavior rates, and an aigent CLI runs or checks a directory with exit codes that say what kind of trouble a run had.

## Altitudes that fit

- design: the problem the change solves, the shape chosen, the alternatives, and what it makes easy or hard next, above function names and flags

## Incidental parts

- the test fixtures under test/scenarios/plugins
- package.json script names
- the boundary test edit

## Size

The plan holds 4 to 10 questions.

## Reading the criteria

A criterion about every question is met when quiz.json has no questions.
A criterion that starts with "When" is met when its condition does not hold.
