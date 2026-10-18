import json
import logging

from src.chunking import chunk_text
from src.config import AppConfig
from src.openrouter import request_chat
from src.repository import save_chunks
from src.storage import save_text

logger = logging.getLogger("TextFlow")

def prepare_translations(text: str, job_id: str, config: AppConfig):
    """
    Splits text into chunks and saves the chunks into the DB
    :param config:
    :param text:
    :return:
    """
    logger.debug("Prepare Translations")
    chunks = chunk_text(text, config.translation.max_chunk_chars)
    save_chunks(chunks, job_id)

def translate_chunks(chunks: list[str], config: AppConfig):
    """
    Translates each chunk and returns the list of chunks
    :param chunks:
    :param config:
    :return:
    """
    translated_chunks = []

    for index, chunk in enumerate(chunks, start=1):
        logger.debug(f"Starting translation request through OpenRouter: {index}/{len(chunks)}" )
        translation = request_translation(chunk, config)
        translated_chunks.append(translation)
        save_text(translation, f"{config.output.directory}/{index}.txt")
    return translated_chunks

def translate_text(text: str, config: AppConfig):
    """
    Automatically splits text into chunks and returns a translation for each chunk combined
    :param config:
    :param text:
    :return:
    """
    logger.debug("Attempting Translations")
    chunks = chunk_text(text, config.translation.max_chunk_chars)
    translated_chunks = translate_chunks(chunks, config)
    return "\n\n".join(translated_chunks)

def request_translation(chunk: str, config: AppConfig):
    """
    Requests a single API call to openRouter and returns the content of the message
    :param config:
    :param chunk:
    :return:
    """
    prompt = f"Translate the following passage into {config.translation.target_language}: \n {chunk}"
    response = request_chat(prompt, config.api)

    choice = response["choices"][0]
    message = choice["message"]["content"]

    logger.debug(f"Model: {response["model"]} | Finish Reason: {choice["finish_reason"]}",)
    logger.info(f"Message: {message}\n")
    logger.info(f"Token usage: {json.dumps(response["usage"], indent=2, ensure_ascii=False)}",)

    return message