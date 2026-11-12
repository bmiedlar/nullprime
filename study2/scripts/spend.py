"""Estimated spend across Study 2 logs. OpenRouter counts twice its list price (the real ratio in the pilot)."""
import pathlib, sys
from inspect_ai.log import read_eval_log
total = 0
for path in sorted(pathlib.Path(sys.argv[1]).glob("*.eval")):
    log = read_eval_log(str(path), header_only=True)
    cost = sum((u.total_cost or 0) for u in log.stats.model_usage.values())
    cost *= 2 if log.eval.model.startswith("openrouter/") else 1
    total += cost
    print(f"{log.eval.model:40} {log.eval.task_args.get('arm')} {log.status:10} ${cost:7.3f}")
print(f"TOTAL ${total:.2f}")
