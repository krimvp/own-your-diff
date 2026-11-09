# Case brief

This brief is for the judge of the quiz plan. The agent that wrote the plan never saw it.

## The target of the change

The skill ships as one plugin tree that Claude Code, Factory Droid, and Codex all read: a session-start hook runs quizgate sync, a PreToolUse guard denies an agent's git push --no-verify and core.hooksPath changes, and an installer adds the plugin to every harness on PATH and trusts the Codex hooks.

## Altitudes that fit

- design: the problem the change solves, the shape chosen, the alternatives, and what it makes easy or hard next, above function names and flags

## Incidental parts

- the JSON fields of plugin.json
- the selftest cases
- the timeout values in hooks.json
- the exact JSON-RPC calls of codex-trust-hooks

## Size

The plan holds 3 to 8 questions.

## Reading the criteria

A criterion about every question is met when quiz.json has no questions.
A criterion that starts with "When" is met when its condition does not hold.
