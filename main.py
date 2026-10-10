import json
import logging
from pathlib import Path

from src.storage import load_file, save_text
from src.translator import translate_text



def set_up_logger():
    Path("debug/logs").mkdir(exist_ok=True, parents=True)

    with open(Path("./logging.json")) as file:
        config = json.load(file)

    logging.config.dictConfig(config=config)




set_up_logger()
text = load_file("test.txt")

translation = translate_text(text)
save_text(translation, "tests/samples/translation.txt")
