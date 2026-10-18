import argparse

from src.CLI.commands import translate_novel, list_pending_chunks, resume_translations, initialize_translation, \
    list_pending_jobs


def add_translate_parser(subparser):
    # Translate Novel
    translate_parser = subparser.add_parser(
        "translate",
        help="Translate a file",
    )
    translate_parser.add_argument(
        "input_file",
        help="Path to the file to translate",
    )
    translate_parser.add_argument(
        "-o", "--output",
        help="Path to save the translation",
    )

    translate_parser.set_defaults(func=translate_novel)

def add_status_parser(subparser):
    # Check Status
    status_parser = subparser.add_parser(
        "status",
        help="Check translation progress",
    )
    status_parser.add_argument(
        "-id",
        help="ID of the translation to check else returns all",
    )
    status_parser.set_defaults(func=list_pending_chunks)

def add_jobs_parser(subparser):
    # Check Status
    job_parser = subparser.add_parser(
        "jobs",
        help="Check jobs progress",
    )
    job_parser.add_argument(
        "-p",
        "--pending",
        action="store_true",
        help="Prints only pending jobs",
    )

    job_parser.set_defaults(func=list_pending_jobs)




def add_continue_parser(subparser):
    # Continue Translations
    continue_parser = subparser.add_parser(
        "continue",
        help="Continue unfinished translations")

    continue_parser.add_argument("job_id")
    continue_parser.set_defaults(func=resume_translations)

def add_prepare_novel_parser(subparser):
    # Continue Translations
    init_parser = subparser.add_parser(
        "prepare",
        help="Chunk a novel but dont send it to openrouter for translations")

    init_parser.add_argument(
        "input_path",
        help="Location of novel",
    )

    init_parser.set_defaults(func=initialize_translation)

def create_parser():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_status_parser(subparser)
    add_translate_parser(subparser)
    add_continue_parser(subparser)
    add_prepare_novel_parser(subparser)
    add_jobs_parser(subparser)
    return parser



