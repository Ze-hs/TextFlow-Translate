
import argparse
import json
import logging.config
from pathlib import Path

from src.config import load_config
from src.storage import load_file, save_text
from src.translator import translate_text


parser = argparse.ArgumentParser(description="Translate a text file.")
parser.add_argument("input", help="Input file path")
parser.add_argument(
    "-o",
    "--output",
    default="translation.txt",
    help="Destination file path (default: translation.txt)",
)

args = parser.parse_args()


Path("debug/logs").mkdir(exist_ok=True, parents=True)
with open("config/logging.json", encoding="utf-8") as file:
    logging_config = json.load(file)


logging.config.dictConfig(logging_config)
config = load_config("config/config.json")


text = load_file(args.input)
translation = translate_text(text, config)
save_text(translation, args.output)
