#!/usr/bin/env bash
# Resume after the deliberate stop on 2026-11-09 ~07:40 (laptop moved). Not a registered file.
# 1) Grok arm L: the 17 items not finished in ...H2Zwi49S...-recovered.eval (23 done there), same settings as run.sh.
# 2) full.sh: skips finished arms, so it continues with Grok F, T, then Opus.
cd /c/Code/Projects/nullprime
{
PYTHONPATH=src .venv/Scripts/inspect.exe eval src/nullprime/study2_eval.py@study2 -T arm=L -T items=runs/study2/items-full.csv \
  --sample-id hard-23,hard-24,hard-25,hard-27,hard-28,hard-29,hard-30,hard-32,hard-33,hard-35,hard-36,hard-37,lookalike-26,lookalike-31,lookalike-34,lookalike-38,lookalike-39 \
  --model grok/grok-4.7 --max-connections 3 --max-samples 3 --cost-limit 1.50 --timeout 600 --retry-on-error 3 \
  --model-cost-config costs.yaml --log-dir runs/study2/full --display plain 2>&1 | tail -6
} > runs/study2/resume.log 2>&1
bash runs/study2/full.sh
