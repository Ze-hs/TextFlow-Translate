from src.repository import delete_job, create_job, get_job, get_all_jobs, update_job_status, get_job_chunks, save_chunks


def test_delete_job_returns_true_for_existing_job(test_db):
    job_id = create_job(
        source_path="novel.txt",
        source_language="Japanese",
        target_language="English",
        database_path=test_db
        )

    assert delete_job(job_id, test_db) is True

def test_create_job_returns_id(test_db):
    job_id = create_job(
        source_path="novel.txt",
        source_language="Japanese",
        target_language="English",
        database_path=test_db
    )

    assert isinstance(job_id, int)
    assert job_id > 0


def test_get_job_returns_existing_job(test_db):
    job_id = create_job(
        source_path="novel.txt",
        source_language="Japanese",
        target_language="English",
        database_path=test_db
    )

    job = get_job(job_id, test_db)

    assert job["id"] == job_id
    assert job["source_path"] == "novel.txt"
    assert job["source_language"] == "Japanese"
    assert job["target_language"] == "English"

def test_get_job_returns_none_for_missing_job(test_db):
    job = get_job(-1, test_db)

    assert job is None

def test_get_all_jobs(test_db):
    for i in range(10):
        create_job(
            source_path="novel.txt",
            source_language="Japanese",
            target_language="English",
            database_path=test_db
        )

    assert len(get_all_jobs(test_db)) == 10

def test_update_job_status(test_db):
    job_id = create_job(
        source_path="novel.txt",
        source_language="Japanese",
        target_language="English",
        database_path=test_db
    )

    update_job_status(job_id, "completed", test_db)

    job = get_job(job_id, test_db)
    assert job["status"] == "completed"


def test_delete_job_returns_false_for_missing_job(test_db):
    assert delete_job(-1, test_db) is False

def test_delete_job_cascades_to_chunks(test_db):
    job_id = create_job(
        source_path="novel.txt",
        source_language="Japanese",
        target_language="English",
        database_path=test_db,
    )

    chunks = ["First chunk of the novel.", "Second chunk of the novel."]
    save_chunks(chunks, job_id, test_db)

    saved_chunks = get_job_chunks(job_id, test_db)

    assert len(saved_chunks) == 2
    assert delete_job(job_id, test_db) is True
    assert get_job_chunks(job_id, test_db) == []


def test_update_job_status_returns_false_for_missing_job(test_db):
    result = update_job_status(-1, "completed", test_db)

    assert result is False


def test_get_all_jobs_returns_empty_list(test_db):
    jobs = get_all_jobs(test_db)
    assert jobs == []

def test_update_job_status_returns_true_for_existing_job(test_db):
    job_id = create_job(
        source_path="novel.txt",
        source_language="Japanese",
        target_language="English",
        database_path=test_db,
    )

    result = update_job_status(job_id, "completed", test_db)

    assert result is True