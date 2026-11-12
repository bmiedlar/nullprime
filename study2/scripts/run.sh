#!/usr/bin/env bash
# Usage: run.sh <items.csv> <log-dir> <limit-dollars> [model ...]   Cheapest models first; stops at the limit.
cd "$(dirname "$0")/../.."
items=$1; logs=$2; limit=$3; shift 3
models=("$@")
[ ${#models[@]} -eq 0 ] && models=(anthropic/claude-haiku-5-5 openai/gpt-6-luna openrouter/deepseek/deepseek-v4-pro
  openrouter/openai/gpt-oss-120b google/gemini-3.8-flash grok/grok-4.7 openai/gpt-6.1-sol google/gemini-4-argon
  anthropic/claude-opus-5-5)
mkdir -p "$logs"
for model in "${models[@]}"; do
  for arm in ${ARMS:-T W}; do
    cost=0.75; [ "$arm" = L ] && cost=1.50
    if PYTHONPATH=src .venv/Scripts/python.exe runs/study2/spend.py "$logs" | grep -qE "^$model +$arm success"; then continue; fi
    spent=$(PYTHONPATH=src .venv/Scripts/python.exe runs/study2/spend.py "$logs" | tail -1 | sed 's/TOTAL \$//')
    if python -c "import sys; sys.exit(0 if $spent >= $limit else 1)"; then echo "STOP: spent \$$spent, limit \$$limit"; exit 0; fi
    PYTHONPATH=src .venv/Scripts/inspect.exe eval src/nullprime/study2_eval.py@study2 -T arm=$arm -T items="$items" \
      --model "$model" --max-connections 3 --max-samples 3 --cost-limit "$cost" --timeout 600 --retry-on-error 3 \
      --model-cost-config costs.yaml --log-dir "$logs" --display plain 2>&1 | tail -4
  done
done
PYTHONPATH=src .venv/Scripts/python.exe runs/study2/spend.py "$logs"
