import pytest

from shared.utils.chunking import chunk_text


def test_chunk_text_splits_large_text() -> None:
    text = "a" * 1200
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) == 3
    assert len(chunks[0]) == 500


def test_chunk_text_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=50, overlap=50)
