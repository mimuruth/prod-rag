# Decisions & trade-offs — prod-rag

## Trade-offs made and why
| Decision | Alternative | Why this way |
|---|---|---|
| Hybrid (BM25 + vector) + reranker | Vector-only | Lexical recall catches exact terms (API names) that embeddings miss; reranker fixes ordering. Cost: two indexes to maintain. |
| Ragas quality gate in CI | Manual spot-checks | Makes regressions impossible to merge silently. Cost: eval adds ~2 min to CI and needs an API key. |
| Refuse-when-unsure | Always answer | A wrong grounded-looking answer is worse than "I don't know" for a docs assistant. Cost: some answerable questions get refused near the margin. |
| Static PNG scoreboard + live Langfuse | Hosted BI dashboard | Zero-cost, always visible in the README; Langfuse covers live drill-down. Cost: the PNG is a snapshot, refreshed by a script. |
| Scale-to-zero Container Apps | Always-on instance | Near-zero idle cost. Cost: ~10 s cold start on the first request after idle. |

## What broke → how it was fixed
- **`nan` eval score passed the CI gate.** A metric that failed to compute returned `nan`, and
  `nan >= threshold` is `False`… but the comparison was inverted so "no signal" read as green.
  **Fix:** treat `nan` as a hard failure explicitly, so missing signal can never pass.
- **Cold-start latency outlier.** A request after idle showed ~14 s (retrieval 9.7 s) in
  `.metrics/requests.jsonl` — the container had scaled to zero. **Fix:** documented as expected
  scale-to-zero behavior; warm p50 is ~2.3 s. A min-replica=1 setting removes it if cost allows.

## If I ran this for 10 more customers
1. **Golden-set floor** — require ≥ 30 QA pairs before a corpus is "green," enforced in CI.
2. **Hosted observability** — one shared Langfuse/App Insights with a read-only stakeholder link.
3. **Corpus→golden coupling** — a check that fails CI if the corpus changes without a golden refresh.
4. **min-replicas policy** — default warm for latency-sensitive tenants; scale-to-zero for dev/demo.
5. **Eval key as a managed secret** — standard secret wiring so the gate never silently skips.
