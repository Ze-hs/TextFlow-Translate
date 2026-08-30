import json
import logging.config
import os
from pathlib import Path
from typing import List

import requests, uuid, json
import spacy
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("TextFlow")

nlp = spacy.load("en_core_web_sm")

def translate_name(name: str, src_lang: str, target_langs: List[str]):
    return azure_translate(name, src_lang, target_langs)[0]["translations"][0]["text"]

def azure_translate(name: str, src_lang: str, target_langs: List[str]):

    key = os.environ.get("AZURE_TRANSLATOR")
    endpoint = "https://api.cognitive.microsofttranslator.com"

    location = os.environ.get("AZURE_REGION")

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': src_lang,
        'to': target_langs
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
                        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': name,
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
    return response

def open_router_call(text: str):
    import requests
    import json

    SECRET_KEY = os.environ.get("OPENROUTER_API_KEY")

    # First API call with reasoning
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {SECRET_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "user",
                    "content": f"Translate the following passage into spanish: {text}"
                }
            ]
        })
    )

    response = response.json()
    response = response['choices'][0]['message']

    return response.get('content')

def load_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def split_text(text: str, threshold: int = 400):
    doc = nlp(text)
    chunks = []
    start = 0

    for sentence in doc.sents:
        end = sentence.end_char

        if end - start > threshold:
            chunks.append(text[start: end])
            start = end

    if start < len(text):
        chunks.append(text[start:])

    return chunks

def translate(text):
    return open_router_call(text)

def save(text: str, path: str):
    with open(path, "a+", encoding="utf-8") as f:
        f.write(text)

def extract_names(text: str):
    doc = nlp(text)
    names = set([ent.text for ent in doc.ents if ent.label_ in {"PERSON", "ORG", "GPE", "LOC", "FAC"}])
    logger.debug(f"Extracted Names: {'\n'.join(names)}\n")
    return names

def set_up_logger():
    Path("debug/logs").mkdir(exist_ok=True, parents=True)

    with open(Path("./logging.json")) as file:
        config = json.load(file)

    logging.config.dictConfig(config=config)

def main():
    azure_translate("小那海あや", "ja", ["en"])
    # set_up_logger()
    # with open("translate.txt", "w", encoding="utf-8") as f:
    #     f.write("")
    #
    # text = load_file("test.txt")
    #
    # chunks = split_text(text)
    # for index, chunk in enumerate(chunks):
    #     logger.debug(f"Chunk {index}")
    #     extract_names(chunk)
    #     translated_text = translate(chunk)
    #     save(translated_text, "translate.txt")

if __name__ == "__main__":
    main()