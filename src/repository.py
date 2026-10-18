import sqlite3
from contextlib import closing
from pathlib import Path

cur = Path(__file__).parent.resolve()
DATABASE_PATH = cur / "../data/translations.db"

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
                model TEXT,
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

def create_job(
    source_path: str,
    source_language: str,
    target_language: str,
):
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO translation_jobs (
                    source_path,
                    source_language,
                    target_language
                )
                VALUES (?, ?, ?)
                """,
                (
                    source_path,
                    source_language,
                    target_language,

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

def save_chunks(chunks: list[str], job_id: str):
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


def update_chunk(
    job_id: int,
    chunk_index: int,
    status: str,
    translated_text: str,
    error_message: str | None = None
) -> bool:
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute(
                """
                UPDATE translation_chunks
                SET status = ?,
                    error_message = ?,
                    translated_text = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE job_id = ?
                  AND chunk_index = ?;
                """,
                (status, error_message, translated_text, job_id, chunk_index)
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

def get_next_chunk_index(job_id):
    with closing(get_connection()) as conn:
        return conn.execute(
            """
            SELECT MIN(chunk_index)
            FROM translation_chunks
            WHERE job_id = ?
              AND status != 'completed'
            """,
            (job_id,)
        ).fetchone()

def get_chunk(job_id: str, chunk_index: str):
    with closing(get_connection()) as conn:
        return conn.execute(
            """
            SELECT *
            FROM translation_chunks
            WHERE job_id = ?
              AND chunk_index = ?
            """,
            (job_id, chunk_index)
        ).fetchone()

def get_all_pending_jobs():
    with closing(get_connection()) as conn:
        return conn.execute(
            """
            SELECT *
            FROM translation_jobs
            WHERE status != 'completed'
            """
        ).fetchall()


def get_all_jobs():
    with closing(get_connection()) as conn:
        return conn.execute(
            """
            SELECT *
            FROM translation_jobs
            """
        ).fetchall()

def delete_job(job_id: str):
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute(
            """
            DELETE FROM translation_jobs
            WHERE id = ?;
            """,
            (job_id,)
            )

            return cursor.rowcount > 0

def get_job_chunk_stats(job_id: int):
    with closing(get_connection()) as conn:
        return conn.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END)
                    AS completed,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END)
                    AS pending,
                SUM(CASE WHEN status = 'processing' THEN 1 ELSE 0 END)
                    AS processing,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END)
                    AS failed
            FROM translation_chunks
            WHERE job_id = ?;
            """,
            (job_id,)
        ).fetchone()