"""Hybrid retrieval: fuse BM25 (keyword) and vector (semantic) results with RRF.

Reciprocal Rank Fusion combines ranked lists without needing comparable scores:
each item's fused score is the sum over lists of 1 / (k + rank).
"""

from __future__ import annotations


def reciprocal_rank_fusion(result_lists: list[list[dict]], k: int = 60) -> list[dict]:
    scores: dict[str, float] = {}
    lookup: dict[str, dict] = {}
    for results in result_lists:
        for rank, item in enumerate(results):
            _id = item["id"]
            lookup[_id] = item
            scores[_id] = scores.get(_id, 0.0) + 1.0 / (k + rank + 1)
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    fused: list[dict] = []
    for _id, score in ranked:
        item = dict(lookup[_id])
        item["rrf_score"] = score
        fused.append(item)
    return fused
