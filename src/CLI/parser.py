import argparse

from src.CLI.commands import translate_novel, initialize_translation, list_jobs, delete_translation, show_job_status, \
    export_translations


def add_prepare_novel_parser(subparser):
    prepare_parser = subparser.add_parser(
        "prepare",
        help="Chunk a novel but dont send it to openrouter for translations")

    prepare_parser.add_argument(
        "input_path",
        help="Location of novel",
    )

    prepare_parser.set_defaults(func=initialize_translation)

def add_translate_parser(subparser):
    # Translate Novel
    translate_parser = subparser.add_parser(
        "translate",
        help="Translate or resume an existing job",
    )
    translate_parser.add_argument(
        "job_id",
        help="Job id",
    )
    translate_parser.add_argument(
        "-o", "--output",
        help="Path to save the translation",
    )

    translate_parser.set_defaults(func=translate_novel)

def add_list_parser(subparser):
    # Check Status
    list_parser = subparser.add_parser(
        "list",
        help="Check translation progress",
    )
    list_parser.add_argument(
        "-p",
        "--pending",
        help="Show only incomplete jobs",
    )

    list_parser.set_defaults(func=list_jobs)

def add_export_parser(subparser):
    # Export job
    export_parser = subparser.add_parser(
        "export",
        help="export translation into a txt file",
    )
    export_parser.add_argument(
        "job_id",
        help="ID of the translation job",
    )

    export_parser.add_argument(
        "-o",
        "--output",
        help="path of the output file",
    )
    export_parser.set_defaults(func=export_translations)


def add_delete_parser(subparser):
    # delete job
    delete_parser = subparser.add_parser(
        "delete",
        help="Delete a job and its chunks"
    )

    delete_parser.add_argument(
        "job_id",
        help="ID of the translation job",
    )
    delete_parser.set_defaults(func=delete_translation)


def add_status_parser(subparser):
    status_parser = subparser.add_parser(
        "status",
        help="Show progress on a job"
    )

    status_parser.add_argument(
        "job_id",
        help="ID of the translation job",
    )
    status_parser.set_defaults(func=show_job_status)



def create_parser():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_prepare_novel_parser(subparser)
    add_translate_parser(subparser)
    add_list_parser(subparser)
    add_export_parser(subparser)
    add_delete_parser(subparser)
    add_status_parser(subparser)

    return parser



