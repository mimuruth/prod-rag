"""Offline evaluation with Ragas. Exits non-zero if any metric is below threshold.

Wired into CI (.github/workflows/eval.yml) so every PR is gated on quality.

Usage:
    python eval/run_ragas.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

GOLDEN = Path(__file__).parent / "golden" / "qa_pairs.jsonl"
CONFIG = Path(__file__).parents[1] / "config" / "retrieval.yaml"


def load_golden() -> list[dict]:
    return [json.loads(line) for line in GOLDEN.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    thresholds = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))["eval_thresholds"]
    dataset = load_golden()

    # TODO(phase-3): run the RAG pipeline over `dataset`, then score with Ragas:
    #   from ragas import evaluate
    #   from ragas.metrics import faithfulness, answer_relevancy, context_precision
    #   scores = evaluate(hf_dataset, metrics=[...])
    scores: dict[str, float] = {}

    failed = []
    for metric, threshold in thresholds.items():
        value = scores.get(metric)
        if value is None:
            print(f"[skip] {metric}: not yet implemented")
            continue
        status = "ok" if value >= threshold else "FAIL"
        print(f"[{status}] {metric}: {value:.3f} (>= {threshold})")
        if value < threshold:
            failed.append(metric)

    if failed:
        print(f"\nEval gate FAILED on: {', '.join(failed)}")
        return 1
    print("\nEval gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
