from rag.observability.metrics import estimate_cost, percentile, summarize


def test_percentile():
    values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    assert percentile(values, 50) == 50
    assert percentile(values, 90) == 90
    assert percentile([], 50) == 0.0


def test_estimate_cost():
    # 1M input tokens + 1M output tokens at the configured rates
    assert round(estimate_cost(1_000_000, 1_000_000), 2) == 0.75


def test_summarize_rolls_up(tmp_path):
    p = tmp_path / "requests.jsonl"
    p.write_text(
        "\n".join(
            [
                '{"latency_ms": 100, "cost_usd": 0.001, "grounded": true, "refused": false}',
                '{"latency_ms": 300, "cost_usd": 0.002, "grounded": false, "refused": true}',
                '{"latency_ms": 200, "error": "TimeoutError"}',
            ]
        ),
        encoding="utf-8",
    )
    s = summarize(p)
    assert s["count"] == 3
    assert s["failure_rate"] == round(1 / 3, 3)
    # of the two non-error rows, one is grounded
    assert s["citation_coverage"] == 0.5
