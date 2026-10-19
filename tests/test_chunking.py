from src.chunking import chunk_text


def test_chunk_text_returns_multiple_chunks():
    text = "First paragraph.\n\n" * 20

    chunks = chunk_text(text, max_size=100)

    assert len(chunks) > 1


def test_chunk_text_preserves_all_text():
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."

    chunks = chunk_text(text, max_size=30)

    assert "".join(chunks) == text


def test_chunk_text_handles_empty_input():
    chunks = chunk_text("", max_size=100)

    assert chunks == []


def test_chunk_text_handles_short_input():
    text = "This is a paragraph."

    chunks = chunk_text(text, max_size=100)

    assert chunks == [text]


def test_chunk_text_respects_max_size():
    text = "First paragraph.\n\n" * 20
    max_size = 100

    chunks = chunk_text(text, max_size=max_size)

    assert all(len(chunk) <= max_size for chunk in chunks)


def test_chunk_text_preserves_order():
    text = (
        "Chapter 1: Start.\n\n"
        "Chapter 2: Middle.\n\n"
        "Chapter 3: End."
    )

    chunks = chunk_text(text, max_size=30)

    assert "".join(chunks) == text