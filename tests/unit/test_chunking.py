import pytest

from src.chunking import chunk_text



def test_short_text_returns_one_chunk():
    assert chunk_text("Hello world.", 20) == ["Hello world."]


def test_oversized_sentence_remains_intact():
    text = "A" * 50 + "."
    result = chunk_text(text, 10)

    assert result == [text]


def test_chunks_respect_target_when_possible():
    text = "Hi. Ok. Yes."
    result = chunk_text(text, 10)

    assert all(
        len(chunk) <= 10 or chunk.strip().endswith(".")
        for chunk in result
    )


def test_empty_text_returns_no_chunks():
    assert chunk_text("", 10) == []


def test_max_size_must_be_positive():
    with pytest.raises(ValueError):
        chunk_text("Hello.", 0)


def test_negative_max_size_raises_error():
    with pytest.raises(ValueError):
        chunk_text("Hello.", -1)