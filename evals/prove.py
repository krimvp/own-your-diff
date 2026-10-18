"""Read an oracle run: every good plan passes the plan check and every bad one fails it."""
import json
import sys
from pathlib import Path

run = Path(sys.argv[1])
cases = [c["id"] for c in json.loads((Path(__file__).parent / "cases.json").read_text())["cases"]]
want = {"oracle-good": True, "oracle-bad": False}
failures = 0
for case in cases:
    for subject, expected in want.items():
        grades = run / case / subject / "trial-01" / "grades" / "plan"
        try:
            active = json.loads((grades / "active.json").read_text())
            grade = json.loads((grades / f"revision-{active['revision']:06d}.json").read_text())
            passed = grade["scores"]["pass"]
            found = grade["evidence"].get("stdout", "").strip().splitlines()[-1]
        except (OSError, KeyError, ValueError) as error:
            passed, found = None, f"no grade: {error}"
        ok = passed is expected
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'}  {case:24} {subject:12} pass={passed}  {found}")
print(f"{len(cases) * 2 - failures} of {len(cases) * 2} as expected")
sys.exit(1 if failures else 0)
