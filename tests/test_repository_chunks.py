from src.repository import (
    create_job,
    save_chunks,
    get_job_chunks, update_chunk, update_chunk_status,
)


def create_test_job(test_db):
    return create_job(
        source_path="novel.txt",
        source_language="Japanese",
        target_language="English",
        database_path=test_db,
    )


def test_save_chunks_stores_all_chunks(test_db):
    job_id = create_test_job(test_db)
    chunks = ["First chunk.", "Second chunk.", "Third chunk."]

    save_chunks(chunks, job_id, test_db)

    saved_chunks = get_job_chunks(job_id, test_db)
    assert len(saved_chunks) == 3
    assert [chunk["source_text"] for chunk in saved_chunks] == chunks


def test_save_chunks_assigns_correct_indices(test_db):
    job_id = create_test_job(test_db)
    chunks = ["First chunk.", "Second chunk.", "Third chunk."]

    save_chunks(chunks, job_id, test_db)

    saved_chunks = get_job_chunks(job_id, test_db)
    assert [chunk["chunk_index"] for chunk in saved_chunks] == [0, 1, 2]


def test_get_job_chunks_returns_chunks_in_order(test_db):
    job_id = create_test_job(test_db)
    chunks = ["First chunk.", "Second chunk.", "Third chunk."]

    save_chunks(chunks, job_id, test_db)

    saved_chunks = get_job_chunks(job_id, test_db)
    assert [chunk["source_text"] for chunk in saved_chunks] == chunks


def test_save_chunks_with_empty_list(test_db):
    job_id = create_test_job(test_db)

    save_chunks([], job_id, test_db)

    assert get_job_chunks(job_id, test_db) == []


def test_get_job_chunks_returns_empty_list_for_missing_job(test_db):
    assert get_job_chunks(-1, test_db) == []


def test_update_chunk_translation(test_db):
    job_id = create_test_job(test_db)
    save_chunks(["Hola"], job_id, test_db)

    result = update_chunk(
        job_id, 0, "completed", "Hello", database_path=test_db
    )

    assert result is True
    chunk = get_job_chunks(job_id, test_db)[0]
    assert chunk["translated_text"] == "Hello"


def test_update_chunk_status(test_db):
    job_id = create_test_job(test_db)
    save_chunks(["Hola"], job_id, test_db)

    result = update_chunk_status(
        job_id, 0, "completed", database_path=test_db
    )

    assert result is True
    chunk = get_job_chunks(job_id, test_db)[0]
    assert chunk["status"] == "completed"
