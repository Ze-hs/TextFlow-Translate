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
    :param text:
    :param job_id:
    :param config:
    :return:
    """
    logger.debug("Preparing translations for job %s", job_id)

    if not text.strip():
        raise ValueError("Cannot prepare a translation from empty text.")

    chunks = chunk_text(text, config.translation.max_chunk_chars)

    save_chunks(chunks, job_id)
    logger.info("Saved %s chunks for job %s", len(chunks), job_id)

def request_translation(chunk: str, config: AppConfig):
    """
    Requests a single API call to openRouter and returns the content of the message
    :param config:
    :param chunk:
    :return:
    """
    if not chunk.strip():
        raise ValueError("Cannot translate an empty chunk.")


    prompt = (
        f"Translate the following passage into "
        f"{config.translation.target_language}:\n{chunk}"
    )

    response = request_chat(prompt, config.api)

    try:
        message = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exception:
        raise ValueError(
            "OpenRouter returned an unexpected response format."
        ) from exception

    # logger.debug(f"Model: {response["model"]} | Finish Reason: {choice["finish_reason"]}",)
    # logger.info(f"Message: {message}\n")
    # logger.info(f"Token usage: {json.dumps(response["usage"], indent=2, ensure_ascii=False)}",)

    return message
