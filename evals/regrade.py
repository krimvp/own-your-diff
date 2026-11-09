"""Write the offline checks for `multeval regrade` of a run, as a JSON list.

usage: python3 evals/regrade.py RUN OUT

The list holds plain, trace, usage, and judge, as evals/build and the run specs define them now.
- plain carries the current quizlint, plain.py, and plain_grade.py, so a changed lint re-scores the run.
- judge carries the current rubric and model. Its case brief comes from the run itself, where the
  run's cases have a judge check. A run of one case without one gets that case's current brief.
  A run of many cases without one gets no judge: one check list cannot hold a brief per case.
"""
import json
import sys
from pathlib import Path

EVALS = Path(__file__).resolve().parent
sys.dont_write_bytecode = True


def build_module():
    from importlib.machinery import SourceFileLoader
    from importlib.util import module_from_spec, spec_from_loader
    loader = SourceFileLoader("build", str(EVALS / "build"))
    module = module_from_spec(spec_from_loader("build", loader))
    loader.exec_module(module)
    return module


def main(run, out):
    build = build_module()
    cases = json.loads((run / "run.json").read_text())["plan"]["suite"]["cases"]
    current = json.loads((EVALS / "suite" / "cases" / cases[0]["id"] / "case.json").read_text())
    judge = next(c for c in current["checks"] if c["grader"] == "judge")
    plain = dict(build.PLAIN_CHECK, files={name: src.read_text() for name, src in build.CHECK_FILES.items()})
    # The free checks go first: multeval regrade stops at the first paid check over the budget.
    checks = [plain, {"grader": "trace", "args": {"skill": "own-your-diff"}}, {"grader": "usage"}]
    stored = all(any(c.get("id") == "judge" for c in case["checks"]) for case in cases)
    if stored:
        checks.append(judge)
    elif len(cases) == 1:
        brief = EVALS / "suite" / "cases" / cases[0]["id"] / "check" / "brief.md"
        checks.append(dict(judge, files={"brief.md": brief.read_text()}))
    else:
        print("evals/regrade: no judge: the run's cases have no judge check, and one check list "
              "cannot give each case its own brief", file=sys.stderr)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(checks, indent=2) + "\n")
    print(", ".join(c.get("id") or c["grader"] for c in checks), file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip())
    main(Path(sys.argv[1]), Path(sys.argv[2]))
