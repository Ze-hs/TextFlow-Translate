
import json
import logging.config
from argparse import ArgumentParser
from pathlib import Path

from src.CLI.parser import create_parser
from src.config import load_config, AppConfig
from src.repository import init_database
from src.storage import load_file, save_text
from src.translator import translate_text


def init_app() -> AppConfig:
    # Init db
    init_database()

    # Init logs
    Path("debug/logs").mkdir(exist_ok=True, parents=True)
    with open("config/logging.json", encoding="utf-8") as file:
        logging_config = json.load(file)

    logging.config.dictConfig(logging_config)
    return load_config("config/config.json")



def main():
    parser = create_parser()
    args = parser.parse_args()

    config = init_app()
    args.func(args, config)
    
    # text = load_file(args.input)
    # translation = translate_text(text, config)
    # save_text(translation, args.output)

if __name__ == "__main__":
    main()