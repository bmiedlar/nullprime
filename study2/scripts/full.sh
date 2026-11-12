#!/usr/bin/env bash
# Study 2 full run, registered at https://osf.io/cujxv (2026-11-07). Cheap models first; Grok and Opus last (top-ups).
cd /c/Code/Projects/nullprime
ARMS="N W L F T" bash runs/study2/run.sh runs/study2/items-full.csv runs/study2/full 300 \
  anthropic/claude-haiku-5-5 openai/gpt-6-luna openrouter/deepseek/deepseek-v4-pro openrouter/openai/gpt-oss-120b \
  google/gemini-3.8-flash openai/gpt-6.1-sol google/gemini-4-argon grok/grok-4.7 anthropic/claude-opus-5-5 \
  > runs/study2/full.log 2>&1
