import json, sys
expect, quiz = (json.load(open(p)) for p in sys.argv[1:3])
n = len(quiz["questions"])
problems = []
if not expect["min"] <= n <= expect["max"]:
    problems.append(f"{n} questions, expected {expect['min']} to {expect['max']}")
if quiz["altitude"] not in expect["altitude"]:
    problems.append(f"altitude {quiz['altitude']}, expected one of {expect['altitude']}")
print("\n".join(f"found: {p}" for p in problems) or f"found: {n} questions at {quiz['altitude']} altitude")
sys.exit(1 if problems else 0)
