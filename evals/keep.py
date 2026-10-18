"""Copy what a reviewer needs from a run into evals/results/<run_id>, for git.

usage: python3 evals/keep.py RUN_DIR

Per attempt: the quiz plan, the judge verdicts, the plan and trace grades, the agent's
trajectory, and the attempt's status and timing. The run manifest, the evidence copies,
and multeval's records stay out: the suite and the lock rebuild them.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

EVALS = Path(__file__).resolve().parent
ATTEMPT_KEYS = ("status", "duration_s", "exit_code", "tries", "cost")


def grade(attempt, check):
    folder = attempt / "grades" / check
    if not (folder / "active.json").exists():
        return None
    active = json.loads((folder / "active.json").read_text())
    revision = json.loads((folder / f"revision-{active['revision']:06d}.json").read_text())
    return {"scores": revision["scores"], "evidence": revision.get("evidence")}


def main(run):
    out = EVALS / "results" / run.name
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    manifest = json.loads((run / "run.json").read_text())
    rows = []
    for attempt in sorted(run.glob("*/*/trial-*")):
        case, subject = attempt.parent.parent.name, attempt.parent.name
        dest = out / case / subject / attempt.name
        dest.mkdir(parents=True)
        status = json.loads((attempt / "attempt.json").read_text())
        (dest / "attempt.json").write_text(json.dumps({k: status.get(k) for k in ATTEMPT_KEYS}, indent=2) + "\n")
        for source, name in ((attempt / "artifacts" / "workdir" / "quiz.json", "quiz.json"),
                             (attempt / "judge.json", "judge.json"),
                             (attempt / "trajectory.json", "trajectory.json")):
            if source.exists():
                shutil.copy(source, dest / name)
        grades = {check: grade(attempt, check) for check in ("plan", "trace")}
        (dest / "grades.json").write_text(json.dumps(grades, indent=2) + "\n")
        quiz = json.loads((dest / "quiz.json").read_text()) if (dest / "quiz.json").exists() else None
        judge = json.loads((dest / "judge.json").read_text()) if (dest / "judge.json").exists() else None
        rows.append((case, subject, attempt.name, grades, quiz, judge))

    lines = [f"# Run {run.name}", "",
             "Subjects: " + ", ".join(f"{s['spec']['id']} ({s['spec']['harness']} {s.get('harness_version')}, {s.get('model')})"
                                      for s in manifest["plan"]["subjects"]) + ".", "",
             "| case | subject | plan | skill loaded | questions | altitude | kinds | judge | judge missed |",
             "|---|---|---|---|---|---|---|---|---|"]
    for case, subject, trial, grades, quiz, judge in rows:
        plan = grades["plan"]["scores"]["pass"] if grades["plan"] else None
        loaded = grades["trace"]["scores"].get("skill_activated") if grades["trace"] else None
        kinds = ", ".join(q["kind"] for q in quiz["questions"]) if quiz else "-"
        missed = ", ".join(str(v["criterion"]) for v in judge["verdicts"] if not v["met"]) if judge else "-"
        score = "-" if not judge or judge["score"] is None else f"{judge['score']:.2f}"
        lines.append(f"| {case} | {subject} | {plan} | {loaded} | {len(quiz['questions']) if quiz else '-'} | "
                     f"{quiz['altitude'] if quiz else '-'} | {kinds} | {score} | {missed or '-'} |")
    stats = subprocess.run([str(EVALS.parent / "skills/own-your-diff/scripts/quizstats"), str(out)],
                           capture_output=True, text=True).stdout
    lines += ["", "## Questions", "", "```", stats.rstrip(), "```", ""]
    (out / "README.md").write_text("\n".join(lines))
    print(out)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
