"""Citation enforcement.

The system must refuse to answer when retrieved chunks do not support a claim,
to avoid hallucination. Every sentence in an answer must map to at least one
retrieved chunk id.

TODO(phase-2): implement claim->evidence mapping and the refusal path.
"""

from __future__ import annotations


def enforce_citations(answer_text: str, retrieved: list[dict]) -> tuple[bool, list[dict]]:
    """Return (is_grounded, citations). If not grounded, caller should refuse."""
    raise NotImplementedError
