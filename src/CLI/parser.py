import argparse

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

def add_continue_parser(subparser):
    # Continue Translations
    subparser.add_parser(
        "continue",
        help="Continue unfinished translations")


def add_chunks_parser(subparser):
    # Continue Translations
    subparser.add_parser(
        "parse",
        help="Parse a novel but dont send it to openrouter for translations")


def create_parser():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_status_parser(subparser)
    add_translate_parser(subparser)
    add_continue_parser(subparser)
    add_chunks_parser(subparser)
    return parser



