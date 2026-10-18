#!/usr/bin/env bash
set -euo pipefail
git config --global user.name fixture
git config --global user.email fixture@example.com
git config --global init.defaultBranch main
git config --global --add safe.directory '*'
mkdir -p /workspace && cd /workspace
tar -xf /fixture/base.tar
git init -q && git add -A && git commit -qm "base"
git init -q --bare /srv/origin.git
git remote add origin /srv/origin.git && git push -q origin main
git switch -qc fix/stale-hookspath
git am -q --committer-date-is-author-date /fixture/patches/*.patch
echo oyd-stale-hookspath >/etc/oyd-case
