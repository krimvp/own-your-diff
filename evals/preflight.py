"""Refuse a paid run whose subjects or judge have no key. multeval would start them anyway.

Delete this once https://github.com/krimvp/multeval/issues/21 lands.
"""
import json
import os
import sys
from pathlib import Path

NEEDS = {
    "claude_code": [["ANTHROPIC_API_KEY"], ["CLAUDE_CODE_OAUTH_TOKEN"]],
    "codex": [["OPENAI_API_KEY"]],
    "droid": [["FACTORY_API_KEY"]],
}
JUDGE = {"anthropic": [["ANTHROPIC_API_KEY"], ["ANTHROPIC_AUTH_TOKEN"]], "openai": [["OPENAI_API_KEY", "OPENAI_BASE_URL"]]}


def missing(options):
    if any(all(os.environ.get(name) for name in names) for names in options):
        return None
    return " or ".join(" and ".join(names) for names in options)


spec = json.loads(Path(sys.argv[1]).read_text())
problems = []
def subject_needs(subject):
    if subject["harness"] == "pi":
        key = subject.get("config", {}).get("provider", {}).get("apiKey", "")
        return [[key[1:]]] if key.startswith("$") else [[]]
    return NEEDS.get(subject["harness"], [[]])


for subject in spec["subjects"]:
    need = missing(subject_needs(subject))
    if need:
        problems.append(f"subject {subject['id']} ({subject['harness']}) needs {need}")
providers = set()
for case in Path(spec["suite"], "cases").glob("*/case.json"):
    for check in json.loads(case.read_text()).get("checks", []):
        if check["grader"] == "judge":
            providers.add(check["args"]["provider"])
for provider in sorted(providers):
    need = missing(JUDGE.get(provider, [[]]))
    if need:
        problems.append(f"the {provider} judge needs {need}")
need = missing([["OPENAI_API_KEY", "OPENAI_BASE_URL"]])
if need:
    problems.append(f"evals/judge.py needs {need}")
if problems:
    sys.exit("evals/eval: not starting a paid run.\n  " + "\n  ".join(problems) + "\nPut the keys in evals/.env (see evals/README.md).")
