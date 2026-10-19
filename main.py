import json
import logging
from pathlib import Path

from src.config import load_config
from src.storage import load_file, save_text
from src.translator import translate_text



def set_up_logger():
    Path("debug/logs").mkdir(exist_ok=True, parents=True)

    with open(Path("config/logging.json")) as file:
        config = json.load(file)
    logging.config.dictConfig(config=config)


def main():
    set_up_logger()

    #
    config = load_config("./config/config.json")
    print(config)
    text = load_file("test.txt")
    #
    translation = translate_text(text, config)
    save_text(translation, "tests/samples/translation.txt")

if __name__ == "__main__":
    main()