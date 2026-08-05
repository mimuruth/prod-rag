"""Render the results scoreboard to docs/prod-rag-results.png.

Numbers mirror the README tables (RAGAS eval + observability rollup). Regenerate with:
    pip install matplotlib
    python scripts/plot_results.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "docs" / "prod-rag-results.png"

# RAGAS scores vs CI gate thresholds
metrics = ["Faithfulness", "Answer\nrelevancy", "Context\nprecision"]
scores = [0.87, 0.85, 1.00]
thresholds = [0.80, 0.78, 0.80]

# Observability latency (ms)
lat_labels = ["p50", "p90"]
lat_values = [2326, 3709]


def main() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    fig.suptitle("prod-rag — evaluation & observability", fontsize=14, fontweight="bold")

    x = range(len(metrics))
    bars = ax1.bar(x, scores, color="#2563eb", width=0.55, label="measured")
    ax1.scatter(x, thresholds, color="#dc2626", marker="_", s=900, linewidths=3, label="gate threshold", zorder=3)
    for b, s in zip(bars, scores):
        ax1.text(b.get_x() + b.get_width() / 2, s + 0.02, f"{s:.2f}", ha="center", fontsize=10)
    ax1.set_ylim(0, 1.15)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(metrics)
    ax1.set_ylabel("score")
    ax1.set_title("RAGAS scores vs CI gate", fontsize=11)
    ax1.legend(loc="lower right", fontsize=9)
    ax1.grid(axis="y", alpha=0.25)

    bars2 = ax2.bar(lat_labels, lat_values, color=["#059669", "#f59e0b"], width=0.5)
    for b, v in zip(bars2, lat_values):
        ax2.text(b.get_x() + b.get_width() / 2, v + 60, f"{v} ms", ha="center", fontsize=10)
    ax2.set_ylim(0, max(lat_values) * 1.25)
    ax2.set_ylabel("latency (ms)")
    ax2.set_title("End-to-end latency · cost $0.00025/req · 100% citations", fontsize=11)
    ax2.grid(axis="y", alpha=0.25)

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=140)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
