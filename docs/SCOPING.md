# Scoping — prod-rag

## Problem
Answer questions from a fixed document corpus with **verifiable** answers: every claim is
grounded in a citation, and the system **refuses** when evidence is insufficient rather than
hallucinating. Treat answer quality as a metric that gates the build, not a vibe.

## In scope
- Hybrid retrieval (BM25 + dense vectors) with cross-encoder reranking.
- Enforced citations + an explicit refusal path.
- A Ragas evaluation harness over a golden set, wired into CI as a **quality gate**.
- Per-request observability: latency (per stage), cost, tokens, grounded/refused, Langfuse trace.
- Containerized deploy (Dockerfile → GHCR on tag → Azure Container Apps).

## Out of scope (deliberately)
- Multi-tenant auth / per-user isolation.
- A document-ingestion UI or connectors (corpus is curated, offline).
- Horizontal scale / HA / autoscaling tuning (single revision, scale-to-zero).
- Answer personalization or conversation memory.

## Success criteria
- CI blocks any PR that drops faithfulness < 0.80, answer-relevancy < 0.78, context-precision < 0.80.
- 100% of returned answers carry a citation **or** are an explicit refusal.
- Each request emits a metrics record and a trace.

## Measured baseline
- Quality: faithfulness **0.87**, answer-relevancy **0.85**, context-precision **1.00** (18 golden pairs).
- Ops: p50 **2,326 ms**, p90 **3,709 ms**, **$0.00025**/request, **100%** citation coverage, **0%** failure.

## Known limitations
- Golden set is 18 pairs — demonstrative, not statistically powered.
- Langfuse is self-hosted for the demo (no public stakeholder URL).
- Corpus is 4 Azure Learn docs + the system doc; broadening the corpus needs a golden-set refresh.
