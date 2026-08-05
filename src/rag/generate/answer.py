"""Answer synthesis: retrieve -> rerank -> enforce citations -> generate.

TODO(phase-1/2): wire the full chain and load the prompt from ``prompts/answer.yaml``.
"""

from __future__ import annotations


def answer(question: str) -> dict:
    """Return {'answer': str, 'citations': list[dict], 'refused': bool}."""
    raise NotImplementedError
