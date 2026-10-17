from src.config import AppConfig
from src.repository import get_all_pending_chunks, get_pending_chunks, create_job, get_all_pending_jobs, get_all_jobs
from src.storage import load_file
from src.translator import prepare_translations
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
    jobs_id = args.id

    if jobs_id is not None:
        pass
    else:
        pass

def initialize_translation(args, config: AppConfig):
    job_id = create_job(args.input_path, config.translation.source_language, config.translation.target_language)
    text = load_file(args.input_path)
    prepare_translations(text, job_id, config)
