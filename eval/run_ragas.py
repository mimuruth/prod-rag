"""Offline evaluation with Ragas. Exits non-zero if any metric is below threshold.

Runs the real RAG pipeline over the golden dataset, scores faithfulness, answer
relevancy, and context precision, and gates the build on configured thresholds.
Wired into CI (.github/workflows/eval.yml) so every PR is quality-gated.

Usage:
    python eval/run_ragas.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import yaml

GOLDEN = Path(__file__).parent / "golden" / "qa_pairs.jsonl"
CONFIG = Path(__file__).parents[1] / "config" / "retrieval.yaml"


def load_golden() -> list[dict]:
    return [json.loads(line) for line in GOLDEN.read_text(encoding="utf-8").splitlines() if line.strip()]


def _build_rows(dataset: list[dict]) -> list[dict]:
    from rag.generate.answer import _load_config, answer, retrieve

    cfg = _load_config()
    rows: list[dict] = []
    for item in dataset:
        question = item["question"]
        retrieved = retrieve(question, cfg)
        result = answer(question)
        rows.append(
            {
                "question": question,
                "answer": result["answer"],
                "contexts": [c["text"] for c in retrieved],
                "ground_truth": item["ground_truth"],
            }
        )
    return rows


def _score(rows: list[dict]) -> dict[str, float]:
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import answer_relevancy, context_precision, faithfulness

    result = evaluate(
        Dataset.from_list(rows),
        metrics=[faithfulness, answer_relevancy, context_precision],
    )
    df = result.to_pandas()
    return {
        "faithfulness": float(df["faithfulness"].mean()),
        "answer_relevancy": float(df["answer_relevancy"].mean()),
        "context_precision": float(df["context_precision"].mean()),
    }


def main() -> int:
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not set - skipping eval gate (no-op). Set the secret to enable it.")
        return 0

    thresholds = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))["eval_thresholds"]
    dataset = load_golden()
    rows = _build_rows(dataset)
    scores = _score(rows)

    failed = []
    for metric, threshold in thresholds.items():
        value = scores.get(metric)
        if value is None:
            print(f"[skip] {metric}: not scored")
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
