"""Hybrid retrieval: fuse BM25 (keyword) and vector (semantic) results.

TODO(phase-2): implement reciprocal rank fusion (RRF) over the two result lists.
"""

from __future__ import annotations


def reciprocal_rank_fusion(result_lists: list[list[dict]], k: int = 60) -> list[dict]:
    raise NotImplementedError
