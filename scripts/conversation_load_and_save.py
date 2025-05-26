import os
import json

CONVERSATION_HISTORY_DIR = "data/conversation_history"

def get_history_path():
    return os.path.join(CONVERSATION_HISTORY_DIR, "history.json")

def load_conversation_history():
    path = get_history_path()
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_conversation_history(history):
    os.makedirs(CONVERSATION_HISTORY_DIR, exist_ok=True)
    with open(get_history_path(), "w") as f:
        json.dump(history, f, indent=4)