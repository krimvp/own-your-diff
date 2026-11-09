"""Prove the checks with fixed plans, at no cost.

usage: python3 evals/prove.py suite OUT    copy evals/suite to OUT without its paid checks
       python3 evals/prove.py check RUN    read an oracle run of that copy

The copy keeps every case, fixture, and check file, and drops each check that calls a
model. So the oracle run grades the real checks, and no judge is called.

In the run, every good plan passes the plan check, and every bad and every wordy plan
fails it. A wordy plan fails on its words alone, and its plain grade shows why.
"""
import json
import shutil
import sys
from pathlib import Path

EVALS = Path(__file__).resolve().parent
PAID = {"judge", "systemone"}


def free_suite(out):
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(EVALS / "suite", out)
    for case in sorted(out.glob("cases/*/case.json")):
        data = json.loads(case.read_text())
        data["checks"] = [c for c in data["checks"] if c["grader"] not in PAID]
        case.write_text(json.dumps(data, indent=2) + "\n")
    print(out)


def grade(attempt, check):
    folder = attempt / "grades" / check
    active = json.loads((folder / "active.json").read_text())
    return json.loads((folder / f"revision-{active['revision']:06d}.json").read_text())


def check_run(run):
    cases = [c["id"] for c in json.loads((EVALS / "cases.json").read_text())["cases"]]
    want = {"oracle-good": True, "oracle-bad": False, "oracle-wordy": False}
    total = failures = 0
    for case in cases:
        for subject, expected in want.items():
            name = subject.replace("oracle-", "oyd-oracle-")
            if not (EVALS / "oracle" / name / "quizzes" / f"{case}.json").exists():
                continue  # no wordy plan for a case that allows no question
            total += 1
            attempt = run / case / subject / "trial-01"
            problems = []
            try:
                plan = grade(attempt, "plan")
                passed = plan["scores"]["pass"]
                found = plan["evidence"].get("stdout", "").strip().splitlines()[-1]
                plain = grade(attempt, "plain")["scores"]
            except (OSError, KeyError, ValueError, IndexError) as error:
                passed, found, plain = None, f"no grade: {error}", {}
            if passed is not expected:
                problems.append(f"pass={passed}, expected {expected}")
            if subject == "oracle-wordy" and passed is False:
                if "more than 40" not in found and "gives it away" not in found:
                    problems.append("it failed for another reason than its words")
                if not (plain.get("prompt_words_max", 0) > 40 and plain.get("giveaways", 0) >= 1):
                    problems.append(f"the plain grade misses the long prompt or the giveaway: {plain}")
            if subject == "oracle-good" and plain.get("giveaways", 0):
                problems.append(f"the plain grade finds a giveaway: {plain}")
            if (attempt / "grades" / "judge").exists():
                problems.append("a judge graded it: the oracle run must call no model")
            failures += bool(problems)
            note = "; ".join(problems) or found
            print(f"{'FAIL' if problems else 'ok  '}  {case:24} {subject:13} pass={passed}  {note}")
    print(f"{total - failures} of {total} as expected")
    return 1 if failures else 0


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in {"suite", "check"}:
        sys.exit(__doc__.strip())
    if sys.argv[1] == "suite":
        free_suite(Path(sys.argv[2]))
    else:
        sys.exit(check_run(Path(sys.argv[2])))
