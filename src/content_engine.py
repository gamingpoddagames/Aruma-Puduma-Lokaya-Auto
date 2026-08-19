import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FACTS_FILE = BASE_DIR / "data" / "facts.json"
HISTORY_FILE = BASE_DIR / "data" / "history.json"


HOOKS = [
    "🤯 ඔබ මේක දැනගෙන හිටියද?",
    "😱 මේක ඇත්ත කියලා විශ්වාස කරන්නත් අමාරුයි!",
    "🧠 අද අපි දැනගන්න යන්නේ පුදුම දෙයක්!",
    "🌍 ලෝකය ගැන ඔබ නොදන්නා දෙයක් මෙන්න!",
    "👀 මේ ගැන බොහෝ දෙනෙක් දන්නේ නැහැ!",
    "✨ පුදුමයි නේද?",
    "🤔 ඔබ මේක කලින් අහලා තිබුණාද?"
]


ENDINGS = [
    "❤️ මේ වගේ තවත් පුදුම Facts සඳහා අපිව Follow කරන්න!",
    "👇 ඔබ මේක කලින් දැනගෙන හිටියාද? Comment කරන්න!",
    "🔄 මේක ඔබේ යාළුවන්ටත් Share කරන්න!",
    "🤯 පුදුම හිතුණා නම් ❤️ එකක් දාන්න!",
    "🌍 තවත් අලුත් Facts සඳහා අපිත් එක්ක එකතු වෙන්න!"
]


def load_json(path):
    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def choose_content():
    facts = load_json(FACTS_FILE)
    history = load_json(HISTORY_FILE)

    used_ids = {
        item.get("id")
        for item in history
        if isinstance(item, dict)
    }

    available = [
        fact for fact in facts
        if fact.get("id") not in used_ids
    ]

    if not available:
        raise RuntimeError(
            "No unused content remains. Add more facts before publishing."
        )

    fact = random.choice(available)
    hook = random.choice(HOOKS)
    ending = random.choice(ENDINGS)

    message = (
        f"{hook}\n\n"
        f"💡 {fact['fact']}\n\n"
        f"{ending}\n\n"
        f"#අරුමපුදුමලෝකය #AmazingFacts #SinhalaFacts"
    )

    return {
        "id": fact["id"],
        "category": fact["category"],
        "topic": fact["topic"],
        "fact": fact["fact"],
        "hook": hook,
        "ending": ending,
        "text": message
    }


def remember_content(content):
    history = load_json(HISTORY_FILE)

    history.append({
        "id": content["id"],
        "category": content["category"],
        "topic": content["topic"],
        "hook": content["hook"],
        "ending": content["ending"],
        "text": content["text"]
    })

    save_json(HISTORY_FILE, history)
