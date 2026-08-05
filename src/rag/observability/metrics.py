"""Quality metrics over time (Project 3, Phase 2).

Track p50/p90 latency (never just the average), cost per request in $/token,
citation coverage, and failure rate.

TODO(phase-3): emit these as Langfuse scores and/or Prometheus metrics.
"""

from __future__ import annotations


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = min(int(round((p / 100) * (len(s) - 1))), len(s) - 1)
    return s[idx]
