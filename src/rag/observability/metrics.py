"""Quality metrics over time (Project 3, Phase 2).

Track p50/p90 latency (never just the average), cost per request in $/token,
citation coverage, and failure rate. Per-request records are appended to a JSONL
file; `summarize()` (and the CLI) roll them up into a dashboard view.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

METRICS_PATH = Path(__file__).resolve().parents[3] / ".metrics" / "requests.jsonl"

# Approx. gpt-4o-mini pricing, USD per 1M tokens. Adjust to your model.
PRICE_PER_1M_INPUT = 0.15
PRICE_PER_1M_OUTPUT = 0.60


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = min(int(round((p / 100) * (len(s) - 1))), len(s) - 1)
    return s[idx]


def estimate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    return (
        prompt_tokens / 1_000_000 * PRICE_PER_1M_INPUT
        + completion_tokens / 1_000_000 * PRICE_PER_1M_OUTPUT
    )


def record_request(record: dict, path: Path = METRICS_PATH) -> None:
    record.setdefault("ts", time.time())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def _load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def summarize(path: Path = METRICS_PATH) -> dict:
    rows = _load(path)
    if not rows:
        return {"count": 0}

    latencies = [r["latency_ms"] for r in rows if "latency_ms" in r]
    costs = [r.get("cost_usd", 0.0) for r in rows]
    errors = sum(1 for r in rows if r.get("error"))
    answered = [r for r in rows if not r.get("error")]
    grounded = sum(1 for r in answered if r.get("grounded"))

    return {
        "count": len(rows),
        "p50_latency_ms": round(percentile(latencies, 50), 1),
        "p90_latency_ms": round(percentile(latencies, 90), 1),
        "avg_cost_usd": round(sum(costs) / len(costs), 6),
        "citation_coverage": round(grounded / len(answered), 3) if answered else 0.0,
        "failure_rate": round(errors / len(rows), 3),
    }


def _main() -> None:
    parser = argparse.ArgumentParser(description="Print the RAG metrics dashboard.")
    parser.add_argument("--path", default=str(METRICS_PATH))
    args = parser.parse_args()
    summary = summarize(Path(args.path))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    _main()
