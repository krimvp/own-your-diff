#!/usr/bin/env python3
"""The `plain` check: how plain the words of a quiz plan are, as multeval scores.

multeval runs this file through its `exec` grader (protocol 1). It reads one request on
stdin and prints one answer on stdout. A `grader.describe` request gets the metrics. A
`grader` request gets the scores of `artifacts/workdir/quiz.json` of the attempt.

The scores come from the lint and language checks of quizlint, the same as
`quizlint --json --plan`. When the shape of the plan is wrong, the words are still
measured where every question has a prompt, key points, and labelled options.
An attempt with no quiz.json gets no scores: a zero would look like good work.
A quiz with no questions scores 0 on every count and mean: it has no hard words.
multeval's gate needs a score from every attempt, so a mean is never left out.

`evals/build` copies this file into every case's check dir, beside quizlint and plain.py.
`evals/keep.py` imports `measure` to backfill old kept runs.
"""
import json
import sys
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

sys.dont_write_bytecode = True

GRADER_ID = "oyd-plain"
GRADER_VERSION = "1"
METRICS = [
    ("questions", "int"),
    ("prompt_words", "float"),
    ("prompt_words_max", "int"),
    ("option_words", "float"),
    ("option_words_max", "int"),
    ("code_names", "float"),
    ("giveaways", "int"),
    ("fluff", "int"),
]


def load_quizlint(path):
    loader = SourceFileLoader("quizlint", str(path))
    module = module_from_spec(spec_from_loader("quizlint", loader))
    loader.exec_module(module)
    return module


def measure(quiz_path, quizlint_path):
    """The scores and the evidence of one quiz file. No file: no scores."""
    quiz_path = Path(quiz_path)
    if not quiz_path.is_file():
        return {}, {"reason": "no quiz.json in the workdir of the attempt"}
    lint = load_quizlint(quizlint_path)
    try:
        quiz = json.loads(quiz_path.read_text())
    except (OSError, ValueError) as error:
        return {}, {"reason": f"quiz.json is not JSON: {error}"}
    problems = lint.lint(quiz, True)
    shape_ok = not problems
    notes, metrics = [], {}
    try:
        language_problems, notes, metrics = lint.language(quiz["questions"])
    except (KeyError, TypeError, AttributeError) as error:
        problems.append(f"the words were not measured: the questions lack {error}")
    else:
        problems += language_problems
    types = dict(METRICS)
    scores = {key: (int(value) if types[key] == "int" else float(value)) for key, value in metrics.items()}
    evidence = {"ok": not problems, "shape_ok": shape_ok, "problems": problems, "notes": notes}
    return scores, evidence


def describe():
    return {"grader_id": GRADER_ID, "grader_version": GRADER_VERSION,
            "metrics": [{"name": name, "type": kind, "direction": "lower", "aggregation": "mean"}
                        for name, kind in METRICS]}


def main():
    request = json.loads(sys.stdin.read())
    if request.get("protocol") != 1 or request.get("grader_interface") != 2:
        sys.exit(f"plain_grade.py: unknown protocol {request.get('protocol')} "
                 f"or grader interface {request.get('grader_interface')}")
    if request["kind"] == "grader.describe":
        answer = describe()
    elif request["kind"] == "grader":
        quiz = Path(request["attempt_dir"]) / "artifacts" / "workdir" / "quiz.json"
        scores, evidence = measure(quiz, Path(__file__).resolve().parent / "quizlint")
        answer = {"grader_id": GRADER_ID, "grader_version": GRADER_VERSION,
                  "scores": scores, "evidence": evidence,
                  # A local script costs nothing. An unknown cost would stop paid work under a budget.
                  "cost": {"usd": 0.0, "source": "adapter"}}
    else:
        sys.exit(f"plain_grade.py: unknown request kind {request['kind']!r}")
    print(json.dumps(answer))


if __name__ == "__main__":
    main()
