"""Tokens per hard number that ended UNKNOWN, long leash (arm L), by model. Reads study2/analysis/items.csv.

    python study2/scripts/chart_unknown_cost.py   ->  docs/img/study2-cost-of-unknown.png
"""
import csv
import statistics as st

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

names = {"claude-haiku-5-5": "Claude Haiku 5.5", "gpt-6-luna": "GPT-6 Luna", "deepseek-v4-pro": "DeepSeek V4 Pro",
         "gpt-oss-120b": "gpt-oss-120b", "gemini-3.8-flash": "Gemini 3.8 Flash", "gpt-6.1-sol": "GPT-6.1 Sol",
         "gemini-4-argon": "Gemini 4 Argon", "grok-4.7": "Grok 4.7", "claude-opus-5-5": "Claude Opus 5.5"}
rows = [r for r in csv.DictReader(open("study2/analysis/items.csv", encoding="utf-8"))
        if r["arm"] == "L" and r["split"] == "hard"]
tok = {m: st.mean(int(r["tokens"]) for r in rows if r["model"] == m and r["outcome"] == "unknown") for m in names}
capped = {m: sum(r["model"] == m and r["stop"] == "cost limit" for r in rows) for m in names}
order = sorted(tok, key=tok.get)
print({names[m]: round(tok[m]) for m in order}, "ratio", round(tok[order[-1]] / tok[order[0]]))

paper, ink, ink2, rule, bar = "#F2F0EA", "#15161A", "#4B4B52", "#D5D1C5", "#2a78d6"
fig, ax = plt.subplots(figsize=(12, 6.5), dpi=150)
fig.patch.set_facecolor(paper)
ax.set_facecolor(paper)
y = range(len(order))
ax.barh(list(y), [tok[m] for m in order], height=0.62, color=bar, edgecolor=paper, linewidth=2)
for i, m in enumerate(order):
    note = f"  {tok[m]:,.0f}" + (f"   (+{capped[m]} never answered: hit the $1.50 cap)" if capped[m] else "")
    ax.text(tok[m], i, note, va="center", ha="left", fontsize=10.5, color=ink)
ax.set_yticks(list(y), [names[m] for m in order], fontsize=11, color=ink)
ax.set_xlim(0, max(tok.values()) * 1.55)
ax.set_xticks([0, 100000, 200000, 300000, 400000, 500000], ["0", "100k", "200k", "300k", "400k", "500k"],
              fontsize=10, color=ink2)
ax.set_xlabel("Average tokens per number (input, re-read context and output)", fontsize=11, color=ink2, labelpad=10)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)
ax.grid(axis="x", color=rule, linewidth=0.8)
ax.set_axisbelow(True)
fig.text(0.015, 0.95, f"The same “I don't know” cost up to {tok[order[-1]] / tok[order[0]]:.0f} times more",
         fontsize=17, color=ink, fontweight="bold", ha="left")
fig.text(0.015, 0.905, "70-digit numbers a Python sandbox can't factor in time · 40 tool calls allowed · "
         "average over the answers that ended UNKNOWN, of 30 numbers per model", fontsize=10.5, color=ink2, ha="left")
fig.text(0.985, 0.03, "miedlar.com/writing", fontsize=9.5, color=ink2, ha="right")
plt.subplots_adjust(left=0.17, right=0.98, top=0.86, bottom=0.13)
fig.savefig("docs/img/study2-cost-of-unknown.png", facecolor=paper)
print("saved")
