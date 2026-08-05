"""Document loaders for Markdown, plain text, and PDFs.

Phase 1: walk a source directory, load supported files, and normalize each to a
common ``Document(text, metadata)`` shape. Metadata carries the source path so the
generator can produce citations.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path

MARKDOWN_SUFFIXES = {".md", ".markdown"}
TEXT_SUFFIXES = {".txt", ".rst"}
PDF_SUFFIXES = {".pdf"}


@dataclass
class Document:
    text: str
    metadata: dict = field(default_factory=dict)


def load_markdown(path: str | Path) -> Document:
    p = Path(path)
    return Document(text=p.read_text(encoding="utf-8"), metadata={"source": str(p), "type": "markdown"})


def load_text(path: str | Path) -> Document:
    p = Path(path)
    return Document(text=p.read_text(encoding="utf-8"), metadata={"source": str(p), "type": "text"})


def load_pdf(path: str | Path) -> Document:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise ImportError("PDF support requires `pypdf` (pip install pypdf).") from exc
    p = Path(path)
    reader = PdfReader(str(p))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return Document(text=text, metadata={"source": str(p), "type": "pdf"})


def load_directory(root: str | Path) -> list[Document]:
    """Recursively load every supported file under ``root``."""
    root = Path(root)
    docs: list[Document] = []
    for file in sorted(root.rglob("*")):
        if not file.is_file():
            continue
        suffix = file.suffix.lower()
        if suffix in MARKDOWN_SUFFIXES:
            docs.append(load_markdown(file))
        elif suffix in TEXT_SUFFIXES:
            docs.append(load_text(file))
        elif suffix in PDF_SUFFIXES:
            docs.append(load_pdf(file))
    return docs


def _main() -> None:
    parser = argparse.ArgumentParser(description="Ingest a directory of docs into the vector store.")
    parser.add_argument("--source", required=True, help="Directory to ingest.")
    args = parser.parse_args()

    from rag.index.vector_store import VectorStore
    from rag.ingest.chunker import chunk_text

    docs = load_directory(args.source)
    store = VectorStore()
    total_chunks = 0
    for doc in docs:
        chunks = chunk_text(doc.text)
        metadatas = [{**doc.metadata, "chunk": i} for i in range(len(chunks))]
        store.add(chunks, metadatas)
        total_chunks += len(chunks)
    print(f"Ingested {len(docs)} documents -> {total_chunks} chunks into the vector store.")


if __name__ == "__main__":
    _main()
