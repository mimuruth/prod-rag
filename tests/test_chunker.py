from rag.ingest.chunker import chunk_text


def test_chunk_overlap_and_size():
    text = " ".join(str(i) for i in range(2000))
    chunks = chunk_text(text, size=700, overlap=100)
    assert len(chunks) >= 3
    # each chunk (except possibly the last) should hold `size` tokens
    assert len(chunks[0].split()) == 700


def test_empty_text():
    assert chunk_text("") == []
