"""Token-aware chunking: ~500–800 tokens per chunk with ~100 tokens overlap."""

from __future__ import annotations

CHUNK_SIZE_TOKENS = 700
CHUNK_OVERLAP_TOKENS = 100


def chunk_text(text: str, size: int = CHUNK_SIZE_TOKENS, overlap: int = CHUNK_OVERLAP_TOKENS) -> list[str]:
    """Split ``text`` into overlapping token windows.

    TODO(phase-1): use a real tokenizer (tiktoken) instead of whitespace splitting.
    """
    words = text.split()
    if not words:
        return []
    chunks: list[str] = []
    step = max(size - overlap, 1)
    for start in range(0, len(words), step):
        window = words[start : start + size]
        chunks.append(" ".join(window))
        if start + size >= len(words):
            break
    return chunks
