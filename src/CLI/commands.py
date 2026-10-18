from src.config import AppConfig
from src.repository import create_job, get_all_pending_jobs, get_all_jobs, \
    get_chunk, update_chunk_status, update_chunk, get_next_chunk_index, delete_job, get_translated_chunks, \
    get_job_chunk_stats, get_job
from src.storage import load_file, save_text
from src.translator import prepare_translations, request_translation
from src.utils.display import print_query_results


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
        print("No more chunks to translate")
        return

    chunk_index = chunk_res[0]
    next_chunk = get_chunk(job_id, chunk_index)

    while next_chunk:
        try:
            # Update db so this chunk is pending
            update_chunk_status(job_id, chunk_index, "processing")
            # translate chunk
            translate_text = request_translation(next_chunk["source_text"], config)
            update_chunk(job_id, chunk_index, "completed", translate_text)

            chunk_index += 1
            next_chunk = get_chunk(job_id, chunk_index)

        except Exception as e:
            update_chunk_status(job_id, chunk_index, "failed", str(e))
            print("Error processing chunk", e)
            return



def initialize_translation(args, config: AppConfig):
    job_id = create_job(args.input_path, config.translation.source_language, config.translation.target_language)
    text = load_file(args.input_path)
    prepare_translations(text, job_id, config)

def delete_translation(args, _):
    if delete_job(args.job_id):
        print("Translation job deleted.")
    else:
        print("Translation job not found.")


def export_translations(args, _):
    job_id = args.job_id

    chunks = get_translated_chunks(job_id)

    if not chunks:
        print("No chunks found for this job.")
        return

    text_chunks = []
    for expected_index, chunk in enumerate(chunks):
        if chunk["chunk_index"] != expected_index:
            print(f"Missing chunk at index {expected_index}.")
            return

        text_chunks.append(chunk["translated_text"])


    translated_text = "\n\n".join(text_chunks)

    output_path = args.output or f"translations/job_{job_id}.txt"

    save_text(translated_text, output_path)

    print(f"Translation exported to {output_path}")

def show_job_status(args, _):
    job = get_job(args.job_id)

    if job is None:
        print(f"Job {args.job_id} not found.")
        return

    stats = get_job_chunk_stats(args.job_id)

    print(f"Job #{job['id']}: {job['source_path']}")
    print(f"Status: {job['status']}")
    print(f"Language: {job['source_language']} -> {job['target_language']}")
    print(f"Model: {job['model']}")
    print(f"Chunks completed: {stats['completed']}/{stats['total']}")