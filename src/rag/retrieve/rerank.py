"""Cross-encoder reranking.

Rescores (query, chunk) pairs jointly for higher precision than bi-encoder
similarity alone. Uses Cohere Rerank if COHERE_API_KEY is set, else a local
sentence-transformers cross-encoder (cached across calls).
"""

from __future__ import annotations

import os

_LOCAL_MODEL = None
_LOCAL_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def _get_local_model():
    global _LOCAL_MODEL
    if _LOCAL_MODEL is None:
        from sentence_transformers import CrossEncoder

        _LOCAL_MODEL = CrossEncoder(_LOCAL_MODEL_NAME)
    return _LOCAL_MODEL


def _rerank_cohere(query: str, chunks: list[dict], top_n: int) -> list[dict]:
    import cohere

    client = cohere.Client(os.environ["COHERE_API_KEY"])
    docs = [c["text"] for c in chunks]
    res = client.rerank(model="rerank-english-v3.0", query=query, documents=docs, top_n=min(top_n, len(docs)))
    out: list[dict] = []
    for r in res.results:
        item = dict(chunks[r.index])
        item["rerank_score"] = r.relevance_score
        out.append(item)
    return out


def _rerank_local(query: str, chunks: list[dict], top_n: int) -> list[dict]:
    model = _get_local_model()
    scores = model.predict([(query, c["text"]) for c in chunks])
    order = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)[:top_n]
    out: list[dict] = []
    for i in order:
        item = dict(chunks[i])
        item["rerank_score"] = float(scores[i])
        out.append(item)
    return out


def rerank(query: str, chunks: list[dict], top_n: int = 5) -> list[dict]:
    if not chunks:
        return []
    if os.getenv("COHERE_API_KEY"):
        return _rerank_cohere(query, chunks, top_n)
    return _rerank_local(query, chunks, top_n)
