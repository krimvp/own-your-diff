#!/usr/bin/env bash
set -uo pipefail
echo "check: quiz.json is a valid plan that fits the change"
[ -f quiz.json ] || { echo "found: no quiz.json in $PWD"; exit 1; }
python3 "$CHECK_DIR/quizlint" --plan quiz.json || exit 1
python3 "$CHECK_DIR/expect.py" "$CHECK_DIR/expect.json" quiz.json
