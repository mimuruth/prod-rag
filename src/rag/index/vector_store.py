"""Vector store wrapper (ChromaDB by default).

TODO(phase-1): embed chunks and persist. Keep the interface storage-agnostic so
Weaviate can be swapped in without touching retrieval code.
"""

from __future__ import annotations


class VectorStore:
    def add(self, chunks: list[str], metadatas: list[dict]) -> None:
        raise NotImplementedError

    def query(self, text: str, k: int = 10) -> list[dict]:
        raise NotImplementedError
