"""
This module handles the persistence of conversation history between the user and the AI agent.

It provides functionality to save and load conversation history to/from JSON files,
ensuring that conversations can persist across multiple sessions. The conversation
history is stored in a structured format that maintains the sequence of interactions
and distinguishes between user and assistant messages.
"""

import os
import json
from typing import List, Dict, Union

# Directory where conversation history files are stored
CONVERSATION_HISTORY_DIR = "data/conversation_history"

def get_history_path() -> str:
    """
    Get the full path to the conversation history file.

    Returns:
        str: Absolute path to the history.json file.
    """
    return os.path.join(CONVERSATION_HISTORY_DIR, "history.json")

def load_conversation_history() -> List[Dict[str, str]]:
    """
    Load the conversation history from the JSON file.

    This function reads the conversation history from disk. If no history file
    exists, it returns an empty list to start a new conversation.

    Returns:
        List[Dict[str, str]]: List of conversation entries, where each entry
            is a dictionary with 'role' and 'message' keys. Example:
            [
                {"role": "user", "message": "Hello"},
                {"role": "assistant", "message": "Hi there!"}
            ]

    Example:
        >>> history = load_conversation_history()
        >>> for entry in history:
        ...     print(f"{entry['role']}: {entry['message']}")
    """
    path = get_history_path()
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_conversation_history(history: List[Dict[str, str]]) -> None:
    """
    Save the conversation history to a JSON file.

    This function persists the conversation history to disk, creating the
    necessary directories if they don't exist. The history is saved in a
    human-readable JSON format with proper indentation.

    Args:
        history (List[Dict[str, str]]): List of conversation entries to save.
            Each entry must be a dictionary with 'role' and 'message' keys.
            The 'role' must be either 'user' or 'assistant'.

    Example:
        >>> history = [
        ...     {"role": "user", "message": "Hello"},
        ...     {"role": "assistant", "message": "Hi there!"}
        ... ]
        >>> save_conversation_history(history)
    """
    os.makedirs(CONVERSATION_HISTORY_DIR, exist_ok=True)
    with open(get_history_path(), "w") as f:
        json.dump(history, f, indent=4)