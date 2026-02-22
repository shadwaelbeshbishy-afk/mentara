import json
import os

def load_json(path, default=None):
    """
    Safely loads a JSON file.
    """
    if not os.path.exists(path):
        return default if default is not None else []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default if default is not None else []
