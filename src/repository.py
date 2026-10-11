import sqlite3
from contextlib import closing
from pathlib import Path

cur = Path(__file__).parent.resolve()
DATABASE_PATH = cur / "data/translations.db"

def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection

def init_database():
    with closing(get_connection()) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS translation_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_path TEXT NOT NULL,
                source_language TEXT NOT NULL,
                target_language TEXT NOT NULL,
                model TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS translation_chunks (
                job_id INTEGER NOT NULL,
                chunk_index INTEGER NOT NULL,
                source_text TEXT NOT NULL,
                translated_text TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                error_message TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            
                PRIMARY KEY (job_id, chunk_index),
                FOREIGN KEY (job_id)
                    REFERENCES translation_jobs(id)
                    ON DELETE CASCADE
            );
        """)

# create_job()	Create a new translation job and return its ID
# get_job()	Retrieve a job's details and status
# update_job_status()	Mark a job as processing, completed, or failed
# create_chunks()	Save all source chunks for a job before translating
# get_pending_chunks()	Retrieve chunks that still need translation
# save_chunk_translation()	Save a successful translation and mark the chunk completed
# update_chunk_status()	Mark a chunk as processing or failed, including its error message
# get_translated_chunks()	Retrieve translations in the correct order for export

def create_job(
    source_path: str,
    source_language: str,
    target_language: str,
    model: str,
):
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO translation_jobs (
                    source_path,
                    source_language,
                    target_language,
                    model
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    source_path,
                    source_language,
                    target_language,
                    model,
                ),
            )

            return cursor.lastrowid


def get_job(job_id: int):
    with closing(get_connection()) as conn:
        return conn.execute(
            """
            SELECT * 
            FROM translation_jobs
            WHERE id = ?;
            """,
            (job_id,)
        ).fetchone()

def update_job_status(job_id: int, status: str) -> bool:
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute(
                """
                UPDATE translation_jobs
                SET status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
                """,
                (status, job_id)
            )

            return cursor.rowcount > 0

def create_chunks(job_id: int, chunks: list[str]):
    with closing(get_connection()) as conn:
        with conn:
            for index, chunk in enumerate(chunks):
                conn.execute(
                    """
                    INSERT INTO translation_chunks (
                        job_id,
                        chunk_index,
                        source_text
                    )
                    VALUES (?, ?, ?);
                    """,
                    (job_id, index, chunk)
                )

def get_pending_chunks(job_id: int):
    with closing(get_connection()) as conn:
        return conn.execute(
            """
            SELECT * 
            FROM translation_chunks
            WHERE job_id = ? AND
            status = 'pending'
            ORDER BY chunk_index;
            """,
            (job_id,)
        ).fetchall()

def save_chunk_translation(
    job_id: int,
    chunk_index: int,
    translated_text: str
):
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute(
                """
                UPDATE translation_chunks
                SET translated_text = ?,
                    status = 'completed',
                    error_message = NULL,
                    updated_at = CURRENT_TIMESTAMP
                WHERE job_id = ?
                  AND chunk_index = ?;
                """,
                (translated_text, job_id, chunk_index)
            )

            return cursor.rowcount > 0

def update_chunk_status(
    job_id: int,
    chunk_index: int,
    status: str,
    error_message: str | None = None
) -> bool:
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute(
                """
                UPDATE translation_chunks
                SET status = ?,
                    error_message = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE job_id = ?
                  AND chunk_index = ?;
                """,
                (status, error_message, job_id, chunk_index)
            )

            return cursor.rowcount > 0

def get_translated_chunks(job_id: int):
    with closing(get_connection()) as conn:
        return conn.execute(
            """
            SELECT *
            FROM translation_chunks
            WHERE job_id = ?
              AND status = 'completed'
            ORDER BY chunk_index;
            """,
            (job_id,)
        ).fetchall()