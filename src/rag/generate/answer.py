"""Answer synthesis (Phase 2): hybrid retrieve -> rerank -> generate -> enforce citations.

Vector + BM25 results are fused with RRF, reranked by a cross-encoder, sent to the
LLM with a grounding prompt, then the response is checked for valid citations. If it
is not grounded, the system refuses rather than risk a hallucination.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import yaml

PROMPT_PATH = Path(__file__).resolve().parents[3] / "prompts" / "answer.yaml"
CONFIG_PATH = Path(__file__).resolve().parents[3] / "config" / "retrieval.yaml"
REFUSAL = "I don't have enough information to answer that."


def _load_prompt() -> dict:
    return yaml.safe_load(PROMPT_PATH.read_text(encoding="utf-8"))


def _load_config() -> dict:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def _format_context(chunks: list[dict]) -> str:
    blocks = []
    for c in chunks:
        source = c["metadata"].get("source", "unknown")
        blocks.append(f"[{c['id']}] (source: {source})\n{c['text']}")
    return "\n\n".join(blocks)


def retrieve(question: str, cfg: dict) -> list[dict]:
    """Hybrid retrieval: vector + BM25 fused by RRF, then cross-encoder rerank."""
    from rag.index.bm25 import BM25Index
    from rag.index.vector_store import VectorStore
    from rag.retrieve.hybrid import reciprocal_rank_fusion
    from rag.retrieve.rerank import rerank

    rc = cfg["retrieval"]
    vector_hits = VectorStore().query(question, k=rc["top_k_vector"])

    bm25 = BM25Index.load()
    bm25_hits = bm25.query(question, k=rc["top_k_bm25"]) if bm25 else []

    result_lists = [vector_hits] + ([bm25_hits] if bm25_hits else [])
    fused = reciprocal_rank_fusion(result_lists, k=rc["rrf_k"])
    return rerank(question, fused, top_n=rc["rerank_top_n"])


def answer(question: str, k: int | None = None) -> dict:
    """Return {'answer', 'citations', 'refused'} grounded in retrieved chunks.

    Emits a Langfuse trace and records latency/cost/grounding metrics per request.
    """
    from dotenv import load_dotenv

    load_dotenv()

    from rag.generate.citations import enforce_citations
    from rag.observability.metrics import estimate_cost, record_request
    from rag.observability.tracing import trace

    cfg = _load_config()
    if k is not None:
        cfg["retrieval"]["top_k_vector"] = k

    started = time.perf_counter()
    with trace("rag.answer", question=question) as span:
        try:
            with span.stage("retrieve"):
                retrieved = retrieve(question, cfg)

            if not retrieved:
                result = {"answer": REFUSAL, "citations": [], "refused": True}
                record_request(
                    {
                        "latency_ms": (time.perf_counter() - started) * 1000,
                        "cost_usd": 0.0,
                        "refused": True,
                        "grounded": False,
                        "stages": span.stage_ms,
                    }
                )
                return result

            prompt = _load_prompt()
            context = _format_context(retrieved)
            messages = [
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"].format(question=question, context=context)},
            ]

            from openai import OpenAI

            client = OpenAI()
            with span.stage("generate"):
                resp = client.chat.completions.create(
                    model="gpt-4o-mini", messages=messages, temperature=0
                )
            text = (resp.choices[0].message.content or "").strip()

            usage = getattr(resp, "usage", None)
            prompt_tokens = getattr(usage, "prompt_tokens", 0) or 0
            completion_tokens = getattr(usage, "completion_tokens", 0) or 0
            cost = estimate_cost(prompt_tokens, completion_tokens)

            if REFUSAL.lower() in text.lower():
                result = {"answer": REFUSAL, "citations": [], "refused": True}
                grounded = False
            else:
                grounded, citations = enforce_citations(text, retrieved)
                if grounded:
                    result = {"answer": text, "citations": citations, "refused": False}
                else:
                    result = {"answer": REFUSAL, "citations": [], "refused": True}

            latency_ms = (time.perf_counter() - started) * 1000
            span.update(
                output=result["answer"],
                metadata={
                    "cost_usd": cost,
                    "grounded": grounded,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                },
            )
            record_request(
                {
                    "latency_ms": latency_ms,
                    "cost_usd": cost,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "refused": result["refused"],
                    "grounded": grounded,
                    "stages": span.stage_ms,
                }
            )
            return result
        except Exception as exc:  # noqa: BLE001 - record failures for the dashboard
            record_request(
                {
                    "latency_ms": (time.perf_counter() - started) * 1000,
                    "cost_usd": 0.0,
                    "error": type(exc).__name__,
                    "stages": span.stage_ms,
                }
            )
            raise


def _main() -> int:
    parser = argparse.ArgumentParser(description="Ask a grounded question.")
    parser.add_argument("question")
    args = parser.parse_args()
    result = answer(args.question)
    print(result["answer"])
    if result["citations"]:
        print("\nSources:")
        for c in result["citations"]:
            print(f"  - {c['source']} [{c['id']}]")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
