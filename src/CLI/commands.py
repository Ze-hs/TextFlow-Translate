import logging

from src.config import AppConfig
from src.repository import create_job, get_all_pending_jobs, get_all_jobs, \
    get_chunk, update_chunk_status, update_chunk, get_next_chunk_index, delete_job, get_translated_chunks, \
    get_job_chunk_stats, get_job, update_job_status
from src.storage import load_file, save_text
from src.translator import prepare_translations, request_translation
from src.utils.display import print_query_results

logger = logging.getLogger("TextFlow")

def list_jobs(args, _):
    if args.pending:
        jobs = get_all_pending_jobs()
        print_query_results(jobs)
    else:
        jobs = get_all_jobs()
        print_query_results(jobs)


def translate_novel(args, config):
    job_id = args.job_id

    chunk_res = get_next_chunk_index(job_id)

    if chunk_res is None:
        logger.info("No more chunks to translate")
        return

    chunk_index = chunk_res[0]
    next_chunk = get_chunk(job_id, chunk_index)

    while next_chunk:
        try:
            update_chunk_status(job_id, chunk_index, "processing")
            translate_text = request_translation(next_chunk["source_text"], config)
            update_chunk(job_id, chunk_index, "completed", translate_text)

        except Exception as e:
            logger.exception("Failed to process job %s, chunk %s",
                job_id, chunk_index)
            update_chunk_status(job_id, chunk_index, "failed", str(e))
            raise

        chunk_index += 1
        next_chunk = get_chunk(job_id, chunk_index)

    update_job_status(job_id, "completed")


def initialize_translation(args, config: AppConfig):
    job_id = create_job(args.input_path, config.translation.source_language, config.translation.target_language)
    text = load_file(args.input_path)
    prepare_translations(text, job_id, config)

def delete_translation(args, _):
    if delete_job(args.job_id):
        logger.info("Translation job deleted.")
    else:
        logger.info("Translation job not found.")


def export_translations(args, _):
    job_id = args.job_id

    chunks = get_translated_chunks(job_id)

    if not chunks:
        logger.info("No chunks found for this job.")
        return

    text_chunks = []
    for expected_index, chunk in enumerate(chunks):
        if chunk["chunk_index"] != expected_index:
            logger.info(f"Missing chunk at index {expected_index}.")
            return

        text_chunks.append(chunk["translated_text"])


    translated_text = "\n\n".join(text_chunks)

    output_path = args.output or f"translations/job_{job_id}.txt"

    save_text(translated_text, output_path)

    logger.info(f"Translation exported to {output_path}")

def show_job_status(args, _):
    job = get_job(args.job_id)

    if job is None:
        logger.info(f"Job {args.job_id} not found.")
        return

    stats = get_job_chunk_stats(args.job_id)

    logger.info(f"Job #{job['id']}: {job['source_path']}")
    logger.info(f"Status: {job['status']}")
    logger.info(f"Language: {job['source_language']} -> {job['target_language']}")
    logger.info(f"Model: {job['model']}")
    logger.info(f"Chunks completed: {stats['completed']}/{stats['total']}")