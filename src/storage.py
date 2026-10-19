from pathlib import Path
import sqlite3



def load_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def save_text(text: str, path: str):
    try:
        with sqlite3.connect("my.db") as conn:
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")

    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
        
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)