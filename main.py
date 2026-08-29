import os

import spacy
from dotenv import load_dotenv

load_dotenv()

nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")

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

    # Extract the assistant message with reasoning_details
    response = response.json()
    response = response['choices'][0]['message']

    return response.get('content')

def load_file(path: str):
    with open(path, "r") as f:
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


def main():
    with open("translate.txt", "w", encoding="utf-8") as f:
        f.write("")

    text = load_file("test.txt")

    chunks = split_text(text)
    for chunk in chunks:
        translated_text = translate(chunk)
        save(translated_text, "translate.txt")


if __name__ == "__main__":
    main()