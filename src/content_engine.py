import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FACTS_FILE = BASE_DIR / "data" / "facts.json"
HISTORY_FILE = BASE_DIR / "data" / "history.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def choose_content():
    facts = load_json(FACTS_FILE)
    history = load_json(HISTORY_FILE)

    used_ids = {
        item["id"]
        for item in history
        if isinstance(item, dict) and "id" in item
    }

    available = [
        fact for fact in facts
        if fact["id"] not in used_ids
    ]

    # If everything has been used, start a new cycle.
    if not available:
        available = facts

    selected = random.choice(available)

    return selected


def remember_content(content):
    history = load_json(HISTORY_FILE)

    history.append({
        "id": content["id"],
        "category": content.get("category", "unknown"),
        "text": content["text"]
    })

    save_json(HISTORY_FILE, history)
