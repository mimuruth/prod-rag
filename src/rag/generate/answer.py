"""Answer synthesis (Phase 1): retrieve top-k -> build grounded prompt -> generate.

Phase 2 will insert hybrid retrieval + reranking and stricter citation enforcement.
"""

from __future__ import annotations

import argparse
import sys
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


def answer(question: str, k: int | None = None) -> dict:
    """Return {'answer', 'citations', 'refused'} grounded in retrieved chunks."""
    from rag.index.vector_store import VectorStore

    cfg = _load_config()
    top_k = k or cfg["retrieval"]["top_k_vector"]

    store = VectorStore()
    retrieved = store.query(question, k=top_k)
    if not retrieved:
        return {"answer": REFUSAL, "citations": [], "refused": True}

    prompt = _load_prompt()
    context = _format_context(retrieved)
    messages = [
        {"role": "system", "content": prompt["system"]},
        {"role": "user", "content": prompt["user"].format(question=question, context=context)},
    ]

    from openai import OpenAI

    client = OpenAI()
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0)
    text = (resp.choices[0].message.content or "").strip()

    refused = REFUSAL.lower() in text.lower()
    citations = [] if refused else [
        {"id": c["id"], "source": c["metadata"].get("source")} for c in retrieved
    ]
    return {"answer": text, "citations": citations, "refused": refused}


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
