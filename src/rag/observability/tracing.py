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
    """Thin, defensive wrapper over a Langfuse span (or a no-op)."""

    def __init__(self, client=None, root=None) -> None:
        self._client = client
        self._root = root
        self.stage_ms: dict[str, float] = {}

    @contextmanager
    def stage(self, name: str):
        start = time.perf_counter()
        cm = None
        if self._client is not None:
            try:
                cm = self._client.start_as_current_span(name=name)
                cm.__enter__()
            except Exception:  # pragma: no cover
                cm = None
        try:
            yield
        finally:
            self.stage_ms[name] = (time.perf_counter() - start) * 1000
            if cm is not None:
                try:
                    cm.__exit__(None, None, None)
                except Exception:  # pragma: no cover
                    pass

    def update(self, **kwargs) -> None:
        if self._root is not None:
            try:
                self._root.update(**kwargs)
            except Exception:  # pragma: no cover
                pass


@contextmanager
def trace(name: str, **metadata):
    client = _client()
    if client is None:
        yield _Trace()
        return

    cm = None
    root = None
    try:
        cm = client.start_as_current_span(name=name, input=metadata)
        root = cm.__enter__()
    except Exception:  # pragma: no cover
        cm = None
    handle = _Trace(client, root)
    try:
        yield handle
    finally:
        if cm is not None:
            try:
                cm.__exit__(None, None, None)
            except Exception:  # pragma: no cover
                pass
        try:
            client.flush()
        except Exception:  # pragma: no cover
            pass
