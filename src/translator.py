import logging

from src.chunking import chunk_text
from src.openrouter import request_chat

logger = logging.getLogger("TextFlow")

def translate_chunks(chunks: list[str]):
    translated_chunks = []

    for index, chunk in enumerate(chunks):
        logger.debug(f"Starting translation request through OpenRouter: {index}/{len(chunks)}" )
        translation = request_translation(chunk)
        translated_chunks.append(translation)

    return translated_chunks

def translate_text(text: str):
    """
    Automatically splits text into chunks and returns a translation for each chunk combined
    :param text:
    :return:
    """
    logger.debug("Attempting Translations")
    chunks = chunk_text(text)
    translated_chunks = translate_chunks(chunks)
    return "\n\n".join(translated_chunks)

def request_translation(chunk: str):
    """
    Requests a single API call to openRouter and returns the content of the message
    :param chunk:
    :return:
    """
    prompt = f"Translate the following passage into Spanish: \n {chunk}"
    response = request_chat(prompt)
    logger.debug(response)
    return response["choices"][0]["message"]["content"]