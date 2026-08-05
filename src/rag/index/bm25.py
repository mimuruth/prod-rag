"""BM25 keyword index (rank-bm25), persisted to disk.

Phase 2: built alongside the vector store during ingest so hybrid retrieval can
fuse sparse keyword matches with dense semantic matches. Chunk ids are shared with
the vector store so the two result lists can be fused by id.
"""

from __future__ import annotations

import pickle
import re
from pathlib import Path

DEFAULT_PATH = str(Path(__file__).resolve().parents[3] / ".bm25" / "index.pkl")


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


class BM25Index:
    def __init__(self) -> None:
        self._bm25 = None
        self._docs: list[dict] = []

    def build(self, chunks: list[str], metadatas: list[dict], ids: list[str]) -> None:
        from rank_bm25 import BM25Okapi

        self._docs = [
            {"id": ids[i], "text": chunks[i], "metadata": metadatas[i]} for i in range(len(chunks))
        ]
        self._bm25 = BM25Okapi([_tokenize(c) for c in chunks])

    def save(self, path: str = DEFAULT_PATH) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("wb") as fh:
            pickle.dump({"bm25": self._bm25, "docs": self._docs}, fh)

    @classmethod
    def load(cls, path: str = DEFAULT_PATH) -> "BM25Index | None":
        p = Path(path)
        if not p.exists():
            return None
        inst = cls()
        with p.open("rb") as fh:
            data = pickle.load(fh)  # noqa: S301 - local, trusted index file
        inst._bm25 = data["bm25"]
        inst._docs = data["docs"]
        return inst

    def query(self, text: str, k: int = 10) -> list[dict]:
        if self._bm25 is None or not self._docs:
            return []
        scores = self._bm25.get_scores(_tokenize(text))
        order = sorted(range(len(self._docs)), key=lambda i: scores[i], reverse=True)[:k]
        return [{**self._docs[i], "score": float(scores[i])} for i in order]
