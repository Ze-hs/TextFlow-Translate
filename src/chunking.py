import logging.config

import spacy
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("TextFlow")

nlp = spacy.load("en_core_web_sm")


def chunk_text(text, max_size: int = 3000):
    """
    Chunks text by sentence size rather than by words. max_size is more of a target rather than limit
    """
    if max_size <= 0:
        raise ValueError("max_size must be positive")

    doc = nlp(text)
    chunks = []
    chunk_start = 0

    for sentence in doc.sents:
        sentence_end = sentence.end_char

        if sentence_end - chunk_start > max_size:
            sentence_start = sentence.start_char

            if sentence_start > chunk_start:
                chunks.append(text[chunk_start:sentence_start])
                chunk_start = sentence_start

        chunks.append(text[chunk_start: sentence_end])
        chunk_start = sentence_end

    if chunk_start < len(text):
      chunks.append(text[chunk_start:])

    return chunks