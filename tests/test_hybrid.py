from rag.retrieve.hybrid import reciprocal_rank_fusion


def test_rrf_rewards_agreement_across_lists():
    vector = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    bm25 = [{"id": "b"}, {"id": "a"}, {"id": "d"}]
    fused = reciprocal_rank_fusion([vector, bm25], k=60)
    ids = [item["id"] for item in fused]
    # a and b appear in both lists near the top -> should rank above c and d
    assert set(ids[:2]) == {"a", "b"}
    assert ids[-1] in {"c", "d"}
    assert all("rrf_score" in item for item in fused)


def test_rrf_single_list_preserves_order():
    single = [{"id": "x"}, {"id": "y"}, {"id": "z"}]
    fused = reciprocal_rank_fusion([single], k=60)
    assert [i["id"] for i in fused] == ["x", "y", "z"]


def test_rrf_empty():
    assert reciprocal_rank_fusion([]) == []
