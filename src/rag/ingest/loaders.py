"""Document loaders for Microsoft Docs, PDFs, Markdown, and GitHub repos.

TODO(phase-1): implement one loader per source type, normalize to a common
`Document(text, metadata={source, url, section})` shape, then hand off to the chunker.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Document:
    text: str
    metadata: dict = field(default_factory=dict)


def load_markdown(path: str) -> list[Document]:
    raise NotImplementedError


def load_pdf(path: str) -> list[Document]:
    raise NotImplementedError


def load_github_repo(url: str) -> list[Document]:
    raise NotImplementedError
