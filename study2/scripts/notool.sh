#!/usr/bin/env bash
# Exploratory no-tool check (not registered), 2026-11-11. Skips model x condition pairs that already succeeded.
cd /c/Code/Projects/nullprime
LOGS=runs/study2/notool
mkdir -p $LOGS
for model in anthropic/claude-haiku-5-5 openai/gpt-6-luna openrouter/deepseek/deepseek-v4-pro openrouter/openai/gpt-oss-120b \
             google/gemini-3.8-flash openai/gpt-6.1-sol google/gemini-4-argon grok/grok-4.7 anthropic/claude-opus-5-5; do
  for cond in X1 X2; do
    if PYTHONPATH=src .venv/Scripts/python.exe - "$LOGS" "$model" "$cond" <<'EOF'
import pathlib, sys
from inspect_ai.log import read_eval_log
d, m, c = sys.argv[1:]
ok = any(l.status == "success" and l.eval.model == m and l.eval.task_args.get("cond") == c
         for l in (read_eval_log(str(p), header_only=True) for p in pathlib.Path(d).glob("*.eval")))
sys.exit(0 if ok else 1)
EOF
    then continue; fi
    PYTHONPATH=src .venv/Scripts/inspect.exe eval runs/study2/notool_eval.py@notool -T cond=$cond --model "$model" \
      --max-connections 12 --cost-limit 0.75 --timeout 600 --retry-on-error 3 --model-cost-config costs.yaml \
      --log-dir $LOGS --display plain 2>&1 | tail -3
  done
done
echo DONE
