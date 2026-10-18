"""Judge every attempt of a run against its case rubric, through an OpenAI-compatible endpoint.

usage: python3 evals/judge.py RUN_DIR

multeval's judges rely on the endpoint enforcing a JSON schema, which Ollama Cloud
ignores (https://github.com/krimvp/multeval/issues/24). This judge states the schema in
the prompt and reads JSON out of a fenced answer. It writes judge.json beside each
attempt and prints a table. Delete it once multeval's judge works on such endpoints.

Reads OPENAI_API_KEY, OPENAI_BASE_URL, and JUDGE_MODEL (default glm-5.3).
"""
import json
import os
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

SUITE = Path(__file__).resolve().parent / "suite"
MODEL = os.environ.get("JUDGE_MODEL", "glm-5.3")

SYSTEM = """You grade a quiz plan that an agent wrote about a code change. You get the criteria
and the file quiz.json. Judge each criterion on its own, strictly, from the file alone.
A criterion about "every question" is met when quiz.json has no questions.

Answer with JSON only, in this shape, one entry per criterion in order:
{"verdicts": [{"criterion": 1, "met": true, "reason": "one short sentence"}]}"""


def ask(criteria, quiz_text):
    user = "Criteria:\n" + "\n".join(f"{n}. {c}" for n, c in enumerate(criteria, 1)) + \
        "\n\nquiz.json:\n" + quiz_text
    body = {"model": MODEL, "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}
    request = urllib.request.Request(
        os.environ["OPENAI_BASE_URL"].rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=600) as response:
        return json.load(response)["choices"][0]["message"]["content"] or ""


def parse(answer, count):
    match = re.search(r"\{.*\}", answer, re.S)
    verdicts = json.loads(match.group(0))["verdicts"] if match else []
    if len(verdicts) != count or not all(isinstance(v.get("met"), bool) for v in verdicts):
        raise ValueError(f"expected {count} verdicts, got {answer[:200]!r}")
    return verdicts


def judge(attempt, criteria):
    quiz = attempt / "artifacts" / "workdir" / "quiz.json"
    if not quiz.exists():
        return {"score": 0.0, "pass": False, "verdicts": [], "error": "no quiz.json"}
    error = None
    for _ in range(2):
        try:
            verdicts = parse(ask(criteria, quiz.read_text()), len(criteria))
            met = sum(v["met"] for v in verdicts)
            return {"model": MODEL, "score": met / len(criteria), "pass": met == len(criteria),
                    "verdicts": [dict(v, text=c) for v, c in zip(verdicts, criteria)]}
        except (ValueError, KeyError, json.JSONDecodeError) as caught:
            error = str(caught)
    return {"model": MODEL, "score": None, "pass": None, "verdicts": [], "error": error}


def main(run):
    rows, by_subject = [], defaultdict(list)
    for attempt in sorted(run.glob("*/*/trial-*")):
        case, subject = attempt.parent.parent.name, attempt.parent.name
        rubric = SUITE / "cases" / case / "check" / "rubric.json"
        if not rubric.exists():
            continue
        result = judge(attempt, json.loads(rubric.read_text()))
        (attempt / "judge.json").write_text(json.dumps(result, indent=2) + "\n")
        by_subject[subject].append(result)
        failed = [v["criterion"] for v in result["verdicts"] if not v["met"]]
        note = result.get("error") or (f"missed {failed}" if failed else "")
        score = "-" if result["score"] is None else f"{result['score']:.2f}"
        rows.append(f"{case:24} {subject:14} {attempt.name:9} score {score:>5}  {note}")
    print("\n".join(rows))
    for subject, results in sorted(by_subject.items()):
        scored = [r for r in results if r["score"] is not None]
        if scored:
            mean = sum(r["score"] for r in scored) / len(scored)
            passed = sum(r["pass"] for r in scored)
            print(f"\n{subject}: judge score {mean:.2f}, all criteria met {passed} of {len(scored)}, unjudged {len(results) - len(scored)}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
