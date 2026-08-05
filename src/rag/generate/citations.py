"""Citation enforcement.

The system must refuse to answer when the generated text is not grounded in the
retrieved chunks, to avoid hallucination. The generator is instructed to cite each
claim inline as ``[chunk_id]``; enforcement checks that at least one cited id maps
to a retrieved chunk. If nothing valid is cited, the caller should refuse.
"""

from __future__ import annotations

import re

_CITE_RE = re.compile(r"\[([0-9a-fA-F][0-9a-fA-F-]{7,})\]")


def enforce_citations(answer_text: str, retrieved: list[dict]) -> tuple[bool, list[dict]]:
    """Return (is_grounded, citations). If not grounded, the caller should refuse."""
    valid_ids = {c["id"] for c in retrieved}
    cited = {m.group(1) for m in _CITE_RE.finditer(answer_text)} & valid_ids
    if not cited:
        return False, []
    citations = [
        {"id": c["id"], "source": c["metadata"].get("source")}
        for c in retrieved
        if c["id"] in cited
    ]
    return True, citations
