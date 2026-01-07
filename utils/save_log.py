import os

def save_raw_response(response: str, filepath: str, note: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(note + "\n\n")
        f.write(response)