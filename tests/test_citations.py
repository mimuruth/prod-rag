from rag.generate.citations import enforce_citations

RETRIEVED = [
    {"id": "11111111-1111-1111-1111-111111111111", "metadata": {"source": "a.md"}},
    {"id": "22222222-2222-2222-2222-222222222222", "metadata": {"source": "b.md"}},
]


def test_grounded_when_valid_id_cited():
    text = "The chunk size is 700 tokens [11111111-1111-1111-1111-111111111111]."
    grounded, citations = enforce_citations(text, RETRIEVED)
    assert grounded is True
    assert citations == [{"id": "11111111-1111-1111-1111-111111111111", "source": "a.md"}]


def test_ungrounded_when_no_citation():
    grounded, citations = enforce_citations("The chunk size is 700 tokens.", RETRIEVED)
    assert grounded is False
    assert citations == []


def test_ungrounded_when_cited_id_not_in_retrieved():
    text = "Answer [99999999-9999-9999-9999-999999999999]."
    grounded, citations = enforce_citations(text, RETRIEVED)
    assert grounded is False
    assert citations == []
