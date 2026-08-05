# Sample corpus document

This is a placeholder document so you can run the Phase 1 ingestion pipeline
end-to-end before wiring up a real corpus.

## Chunking

This RAG system chunks documents into windows of roughly 500 to 800 tokens with
about 100 tokens of overlap between adjacent chunks. Overlap preserves context that
would otherwise be split across a chunk boundary.

## Retrieval

Phase 1 uses vector similarity search over a ChromaDB collection, embedded locally
with the `all-MiniLM-L6-v2` sentence-transformers model, and returns the top-k
chunks. Phase 2 adds BM25 keyword search fused with the vector results, followed by
a cross-encoder reranker.

## Grounding

The generator answers strictly from the retrieved context and refuses when the
context is insufficient, to avoid hallucination.
