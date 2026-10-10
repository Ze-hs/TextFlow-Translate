from pathlib import Path


def load_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def save_text(text: str, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)