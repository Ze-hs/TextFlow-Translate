from src.config import AppConfig
from src.repository import get_all_pending_chunks, get_pending_chunks, create_job, get_all_pending_jobs, get_all_jobs, \
     get_chunk, update_chunk_status, update_chunk, get_next_chunk_index
from src.storage import load_file
from src.translator import prepare_translations, request_translation
from src.utils.display import print_query_results


def list_pending_jobs(args, _):
    if args.pending:
        jobs = get_all_pending_jobs()
        print_query_results(jobs)
    else:
        jobs = get_all_jobs()
        print_query_results(jobs)

def list_pending_chunks(args, _):
    chunk_id = args.id
    if chunk_id is None:
        chunks = get_all_pending_chunks()
        print_query_results(chunks)
    else:
        print_query_results(get_pending_chunks(chunk_id))

def translate_novel(args, config):
    pass

def resume_translations(args, config):
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
