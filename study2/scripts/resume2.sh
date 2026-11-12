#!/usr/bin/env bash
# Resume after the second deliberate stop on 2026-11-09 ~17:29 (laptop moved). Not a registered file.
# 1) Opus arm L: the 2 items not finished in ...3jDJWUCF... (38 done there; raw log, status "started"), same settings as run.sh.
# 2) full.sh: skips finished arms, so it continues with Opus F, T.
cd /c/Code/Projects/nullprime
{
PYTHONPATH=src .venv/Scripts/inspect.exe eval src/nullprime/study2_eval.py@study2 -T arm=L -T items=runs/study2/items-full.csv \
  --sample-id hard-36,hard-37 \
  --model anthropic/claude-opus-5-5 --max-connections 3 --max-samples 3 --cost-limit 1.50 --timeout 600 --retry-on-error 3 \
  --model-cost-config costs.yaml --log-dir runs/study2/full --display plain 2>&1 | tail -6
} > runs/study2/resume2.log 2>&1
bash runs/study2/full.sh
