"""Per-request tracing (Project 3, Phase 1).

Records each request's stages (retrieve, rerank, generate), the prompt, response,
and token usage to Langfuse. Fully optional and defensive: if Langfuse isn't
installed or configured, tracing degrades to a no-op so the pipeline never breaks.
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager


def _client():
    if not (os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")):
        return None
    try:
        from langfuse import Langfuse

        return Langfuse()
    except Exception:  # pragma: no cover - Langfuse optional/version-variant
        return None


class _Trace:
    """Thin, defensive wrapper over a Langfuse trace (or a no-op)."""

    def __init__(self, lf_trace=None) -> None:
        self._t = lf_trace
        self.stage_ms: dict[str, float] = {}

    @contextmanager
    def stage(self, name: str):
        start = time.perf_counter()
        child = None
        if self._t is not None:
            try:
                child = self._t.span(name=name)
            except Exception:  # pragma: no cover
                child = None
        try:
            yield
        finally:
            self.stage_ms[name] = (time.perf_counter() - start) * 1000
            if child is not None:
                try:
                    child.end()
                except Exception:  # pragma: no cover
                    pass

    def update(self, **kwargs) -> None:
        if self._t is not None:
            try:
                self._t.update(**kwargs)
            except Exception:  # pragma: no cover
                pass


@contextmanager
def trace(name: str, **metadata):
    client = _client()
    lf_trace = None
    if client is not None:
        try:
            lf_trace = client.trace(name=name, metadata=metadata)
        except Exception:  # pragma: no cover
            lf_trace = None
    handle = _Trace(lf_trace)
    try:
        yield handle
    finally:
        if client is not None:
            try:
                client.flush()
            except Exception:  # pragma: no cover
                pass
