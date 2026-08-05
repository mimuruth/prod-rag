"""Cross-encoder reranking.

Rescores (query, chunk) pairs jointly for higher precision than bi-encoder
similarity alone. Uses Cohere Rerank if COHERE_API_KEY is set, else a local
sentence-transformers cross-encoder.

TODO(phase-2): implement both backends behind a single `rerank()` call.
"""

from __future__ import annotations


def rerank(query: str, chunks: list[dict], top_n: int = 5) -> list[dict]:
    raise NotImplementedError
