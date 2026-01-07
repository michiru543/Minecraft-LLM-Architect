import json
import os

def load_material_map(file_path: str) -> dict:
    """
    Load the material mapping table, skip the first line, and return the dictionary form: {resource ID: material name}
    """
    material_map = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()[1:]  # Skip the first line of headings
        for line in lines:
            if "=" in line:
                key, name = line.strip().split("=", 1)
                material_map[key.strip()] = key.strip()
    return material_map


def load_json_file(filepath):
    """
    Securely read JSON files: make sure they exist, are not empty, and are formatted correctly.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"[ERROR] JSON file not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    if not content:
        raise ValueError(f"[ERROR] JSON file is empty: {filepath}")

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"[ERROR] Invalid JSON format in {filepath}: {str(e)}")

    return data


def load_text_file(filepath):
    """
    Safe reading of text (e.g. Python / prompt / Markdown) files: make sure the file exists and is not empty.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"[ERROR] File not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    if not content:
        raise ValueError(f"[ERROR] File is empty: {filepath}")

    return content