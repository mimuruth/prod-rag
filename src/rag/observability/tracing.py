"""Per-request tracing (Project 3, Phase 1).

Every request should record: retrieved chunks, reranker ordering, the exact prompt
sent to the LLM, the response, and token usage. Backed by Langfuse (self-hosted).

TODO(phase-3): implement a decorator/context-manager that spans each pipeline stage.
"""

from __future__ import annotations

from contextlib import contextmanager


@contextmanager
def trace(name: str, **metadata):
    # TODO: start a Langfuse span here.
    yield
