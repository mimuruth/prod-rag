"""Vector store wrapper (ChromaDB, persistent).

Phase 1: embed chunks with a local sentence-transformers model (no API key needed)
and persist to disk. The interface stays storage-agnostic so Weaviate can replace
Chroma in Phase 2 without touching retrieval code.
"""

from __future__ import annotations

import uuid
from pathlib import Path

DEFAULT_PERSIST_DIR = str(Path(__file__).resolve().parents[3] / ".chroma")
DEFAULT_COLLECTION = "docs"
DEFAULT_EMBED_MODEL = "all-MiniLM-L6-v2"


class VectorStore:
    def __init__(
        self,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        collection: str = DEFAULT_COLLECTION,
        embed_model: str = DEFAULT_EMBED_MODEL,
    ) -> None:
        import chromadb
        from chromadb.utils import embedding_functions

        self._client = chromadb.PersistentClient(path=persist_dir)
        self._embed = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embed_model)
        self._collection = self._client.get_or_create_collection(
            name=collection, embedding_function=self._embed
        )

    def add(self, chunks: list[str], metadatas: list[dict]) -> None:
        if not chunks:
            return
        ids = [str(uuid.uuid4()) for _ in chunks]
        self._collection.add(documents=chunks, metadatas=metadatas, ids=ids)

    def query(self, text: str, k: int = 10) -> list[dict]:
        res = self._collection.query(query_texts=[text], n_results=k)
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        dists = res.get("distances", [[]])[0]
        ids = res.get("ids", [[]])[0]
        return [
            {"id": ids[i], "text": docs[i], "metadata": metas[i], "distance": dists[i]}
            for i in range(len(docs))
        ]
