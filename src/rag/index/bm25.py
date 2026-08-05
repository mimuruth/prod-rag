"""BM25 keyword index (rank-bm25).

TODO(phase-2): build the sparse index alongside the vector store so hybrid
retrieval can fuse keyword + semantic results.
"""

from __future__ import annotations


class BM25Index:
    def add(self, chunks: list[str], metadatas: list[dict]) -> None:
        raise NotImplementedError

    def query(self, text: str, k: int = 10) -> list[dict]:
        raise NotImplementedError
