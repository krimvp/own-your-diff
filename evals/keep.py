"""Keep what a reviewer needs from a run in evals/results/<run_id>, for git, and redo evals/QUALITY.md.

usage: python3 evals/keep.py RUN_DIR REPORT_JSON    keep a run; REPORT_JSON is `multeval report RUN_DIR --json`
       python3 evals/keep.py --quality              redo evals/QUALITY.md from evals/results

Per attempt: the quiz plan, the plan, trace, plain, judge, and usage grades, the agent's
trajectory, and the attempt's status and timing. The run manifest, the evidence copies,
and multeval's records stay out: the suite and the lock rebuild them.

Per run: summary.json holds the means of each subject, as multeval's report gives them, and
README.md holds a table of every attempt. QUALITY.md holds one row per kept run and subject.

A run kept before the grades moved into multeval has no summary.json. --quality writes one
from its kept files: plan and trace from grades.json, the judge from judge.json (an older
rubric), plain from quiz.json with today's quizlint, and usage from attempt.json, which is
what multeval's usage grader reads. A value that the files do not hold stays empty.
"""
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EVALS = Path(__file__).resolve().parent
ROOT = EVALS.parent
QUIZLINT = ROOT / "skills" / "own-your-diff" / "scripts" / "quizlint"
ATTEMPT_KEYS = ("status", "duration_s", "exit_code", "tries", "cost")
CHECKS = ("plan", "trace", "plain", "judge", "usage")
PLAIN = ("questions", "prompt_words", "prompt_words_max", "option_words", "option_words_max",
         "code_names", "giveaways", "fluff")
USAGE = ("duration_s", "input_tokens", "output_tokens")
sys.dont_write_bytecode = True
sys.path.insert(0, str(EVALS))
from plain_grade import measure  # noqa: E402


def grade(attempt, check):
    folder = attempt / "grades" / check
    if not (folder / "active.json").exists():
        return None
    active = json.loads((folder / "active.json").read_text())
    revision = json.loads((folder / f"revision-{active['revision']:06d}.json").read_text())
    return {"scores": revision["scores"], "evidence": revision.get("evidence")}


def mean(values):
    values = [float(v) for v in values if v is not None]
    return round(sum(values) / len(values), 3) if values else None


def git(*args):
    out = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else None


def run_date(run_id):
    return datetime.strptime(run_id[:15], "%Y%m%d-%H%M%S").replace(tzinfo=timezone.utc).strftime("%Y-%m-%d")


def from_report(report):
    """The means of each subject, read from multeval's JSON report."""
    subjects = {}
    for subject in report["subjects"]:
        metrics = {m["name"]: m["mean"] for m in subject["metrics"]}
        subjects[subject["subject_id"]] = {
            "attempts": subject["attempts"],
            "plan_pass": metrics.get("plan.pass"),
            "skill_loaded": metrics.get("trace.skill_activated"),
            "judge_score": metrics.get("judge.score"),
            "plain": {name: metrics.get(f"plain.{name}") for name in PLAIN},
            "usage": {name: metrics.get(f"usage.{name}") for name in USAGE},
        }
    return subjects


def keep(run, report_path):
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
                             (attempt / "trajectory.json", "trajectory.json")):
            if source.exists():
                shutil.copy(source, dest / name)
        grades = {check: grade(attempt, check) for check in CHECKS}
        (dest / "grades.json").write_text(json.dumps(grades, indent=2) + "\n")
        quiz = json.loads((dest / "quiz.json").read_text()) if (dest / "quiz.json").exists() else None
        rows.append((case, subject, attempt.name, grades, quiz))

    subjects = from_report(json.loads(Path(report_path).read_text()))
    models = {((g["judge"] or {}).get("evidence") or {}).get("model") for *_, g, _ in rows}
    judge_model = ", ".join(sorted(m for m in models if m)) or None
    dirty = bool(git("status", "--porcelain", "--", "skills", "evals/suite"))
    summary = {
        "run": run.name, "date": run_date(run.name), "source": "multeval report",
        "plugin_version": json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())["version"],
        "commit": git("rev-parse", "--short", "HEAD"), "dirty": dirty,
        "judge_model": judge_model, "subjects": subjects,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_readme(out, manifest, rows)
    write_quality()
    print(out)


def cell(value, digits=2):
    if value is None:
        return "-"
    if isinstance(value, bool):
        return str(value)
    return f"{value:.{digits}f}" if isinstance(value, float) else str(value)


def write_readme(out, manifest, rows):
    lines = [f"# Run {out.name}", "",
             "Subjects: " + ", ".join(f"{s['spec']['id']} ({s['spec']['harness']} {s.get('harness_version')}, {s.get('model')})"
                                      for s in manifest["plan"]["subjects"]) + ".", "",
             "| case | subject | trial | plan | skill loaded | questions | altitude | kinds | prompt words | option words | code names | giveaways | fluff | judge | judge missed |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for case, subject, trial, grades, quiz in rows:
        score = lambda check, name: (grades[check] or {}).get("scores", {}).get(name)
        kinds = ", ".join(q["kind"] for q in quiz["questions"]) if quiz else "-"
        criteria = ((grades["judge"] or {}).get("evidence") or {}).get("criteria") or []
        missed = ", ".join(str(n) for n, c in enumerate(criteria, 1) if not c.get("met")) or "-"
        lines.append(" | ".join([
            f"| {case}", subject, trial, cell(score("plan", "pass")), cell(score("trace", "skill_activated")),
            cell(len(quiz["questions"]) if quiz else None), quiz["altitude"] if quiz else "-", kinds,
            cell(score("plain", "prompt_words"), 1), cell(score("plain", "option_words"), 1),
            cell(score("plain", "code_names")), cell(score("plain", "giveaways")), cell(score("plain", "fluff")),
            cell(score("judge", "score")), missed]) + " |")
    stats = subprocess.run([str(QUIZLINT.parent / "quizstats"), str(out)], capture_output=True, text=True).stdout
    lines += ["", "## Questions", "", "```", stats.rstrip(), "```", ""]
    (out / "README.md").write_text("\n".join(lines))


def backfill(out):
    """A summary of a run kept before the grades moved into multeval, from its kept files only."""
    by_subject = {}
    for attempt in sorted(out.glob("*/*/trial-*")):
        status = json.loads((attempt / "attempt.json").read_text())
        if status.get("status") == "infra_error":
            continue  # multeval grades no infra_error attempt
        grades = json.loads((attempt / "grades.json").read_text()) if (attempt / "grades.json").exists() else {}
        judge = json.loads((attempt / "judge.json").read_text()) if (attempt / "judge.json").exists() else {}
        plain, _ = measure(attempt / "quiz.json", QUIZLINT)
        cost = status.get("cost") or {}
        by_subject.setdefault(attempt.parent.name, []).append({
            "plan": ((grades.get("plan") or {}).get("scores") or {}).get("pass"),
            "skill": ((grades.get("trace") or {}).get("scores") or {}).get("skill_activated"),
            "judge": judge.get("score"), "judge_model": judge.get("model"), "plain": plain,
            "usage": {"duration_s": status.get("duration_s"), "input_tokens": cost.get("prompt_tokens"),
                      "output_tokens": cost.get("completion_tokens")},
        })
    subjects = {name: {
        "attempts": len(items),
        "plan_pass": mean(i["plan"] for i in items),
        "skill_loaded": mean(i["skill"] for i in items),
        "judge_score": mean(i["judge"] for i in items),
        "plain": {m: mean(i["plain"].get(m) for i in items) for m in PLAIN},
        "usage": {m: mean(i["usage"][m] for i in items) for m in USAGE},
    } for name, items in sorted(by_subject.items())}
    models = {i["judge_model"] for items in by_subject.values() for i in items if i["judge_model"]}
    return {
        "run": out.name, "date": run_date(out.name),
        "source": "backfilled from the kept files; the judge is evals/judge.py with an older rubric",
        "plugin_version": None, "commit": None, "dirty": None,
        "judge_model": ", ".join(sorted(models)) or None, "subjects": subjects,
    }


def write_quality():
    lines = ["# Quiz quality over time", "",
             "One row per kept run and subject, oldest first. `evals/eval keep` writes it from each run's "
             "`summary.json`. Rates are the share of attempts, and the other numbers are means over attempts.", "",
             "Plain counts words in the plan's prompts and options, code names per question, and give-away "
             "options and filler words per quiz. Lower is better. Usage is per attempt.", "",
             "| run | date | version | commit | subject | attempts | plan pass | skill loaded | judge | questions "
             "| prompt words | prompt max | option words | option max | code names | giveaways | fluff "
             "| duration s | input tokens | output tokens |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    any_old = False
    for out in sorted(p for p in (EVALS / "results").iterdir() if p.is_dir()):
        path = out / "summary.json"
        if not path.exists():
            path.write_text(json.dumps(backfill(out), indent=2) + "\n")
        summary = json.loads(path.read_text())
        old = summary["source"] != "multeval report"
        any_old = any_old or old
        commit = summary["commit"] and summary["commit"] + ("+" if summary.get("dirty") else "")
        for subject, s in summary["subjects"].items():
            p, u = s["plain"], s["usage"]
            judge = cell(s["judge_score"]) + ("*" if old and s["judge_score"] is not None else "")
            lines.append(" | ".join([
                f"| {summary['run']}", summary["date"], summary["plugin_version"] or "-", commit or "-", subject,
                str(s["attempts"]), cell(s["plan_pass"]), cell(s["skill_loaded"]), judge,
                cell(p["questions"], 1), cell(p["prompt_words"], 1), cell(p["prompt_words_max"], 1),
                cell(p["option_words"], 1), cell(p["option_words_max"], 1), cell(p["code_names"]),
                cell(p["giveaways"]), cell(p["fluff"]), cell(u["duration_s"], 0),
                cell(u["input_tokens"], 0), cell(u["output_tokens"], 0)]) + " |")
    lines.append("")
    if any_old:
        lines += ["Runs marked * in the judge column were kept before the grades moved into multeval. "
                  "Their judge was evals/judge.py, with a rubric that lacked the code-closed and plain-English "
                  "criteria. Their plain numbers come from their quiz.json with today's quizlint. Their usage "
                  "comes from the kept attempt, as multeval's usage grader reads it.", ""]
    lines += ["A commit with + was kept from a tree with changes to the skill or the suite.", ""]
    (EVALS / "QUALITY.md").write_text("\n".join(lines))


if __name__ == "__main__":
    if sys.argv[1:] == ["--quality"]:
        write_quality()
        print(EVALS / "QUALITY.md")
    elif len(sys.argv) == 3:
        keep(Path(sys.argv[1]), sys.argv[2])
    else:
        sys.exit(__doc__.strip())
