import json
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

CONTENT_FILE = BASE_DIR / "data" / "content.json"
HISTORY_FILE = BASE_DIR / "data" / "history.json"


HOOKS = [
    "🤯 ඔබ මේක දැනගෙන හිටියාද?",
    "😱 මේක ඇත්ත කියලා විශ්වාස කරන්නත් අමාරුයි!",
    "👀 මේ ගැන බොහෝ දෙනෙක් දන්නේ නැහැ!",
    "🧠 අද අපි දැනගන්න යන්නේ පුදුම දෙයක්!",
    "✨ ලෝකය ඇත්තටම පුදුමයි!",
    "😲 මේ තොරතුර ඔබව පුදුම කරයි!",
    "💡 අද දැනගන්න වටිනා දෙයක් මෙන්න!"
]


CTAS = [
    "👇 ඔබ මේක කලින් දැනගෙන හිටියාද? Comment කරන්න!",
    "❤️ මේ වගේ තවත් දේවල් සඳහා අපිව Follow කරන්න!",
    "🔄 මේක ඔබේ යාළුවන්ටත් Share කරන්න!",
    "🤯 පුදුම හිතුණා නම් ❤️ එකක් දාන්න!",
    "👇 ඔබේ අදහස Comment කරන්න!"
]


HASHTAGS = [
    "#අරුමපුදුමලෝකය #SinhalaFacts",
    "#අරුමපුදුමලෝකය #AmazingFacts",
    "#අරුමපුදුමලෝකය #දැනගමු",
    "#AmazingWorld #Sinhala"
]


FORMATS = [
    "fact",
    "question",
    "quiz"
]


def load_json(path):
    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def choose_unused_content():

    content = load_json(CONTENT_FILE)
    history = load_json(HISTORY_FILE)

    used = {
        item.get("content_id")
        for item in history
        if isinstance(item, dict)
    }

    available = [
        item
        for item in content
        if item["id"] not in used
    ]

    if not available:
        raise RuntimeError(
            "No unused content remains."
        )

    return random.choice(available)


def make_text_post(item):

    content_format = random.choice(FORMATS)
    hook = random.choice(HOOKS)
    cta = random.choice(CTAS)
    hashtag = random.choice(HASHTAGS)

    if content_format == "question":

        text = (
            f"🤔 {item['title']}\n\n"
            f"{item['question']}\n\n"
            f"💬 ඔබේ පිළිතුර Comment කරන්න!\n\n"
            f"{cta}\n\n"
            f"{hashtag}"
        )

    elif content_format == "quiz":

        text = (
            f"🧩 පොඩි Quiz එකක්!\n\n"
            f"{item['question']}\n\n"
            f"👇 පිළිතුර Comment කරන්න!\n\n"
            f"💡 නිවැරදි පිළිතුර: "
            f"{item['answer']}\n\n"
            f"{cta}\n\n"
            f"{hashtag}"
        )

    else:

        text = (
            f"{hook}\n\n"
            f"{item['emoji']} {item['title']}\n\n"
            f"💡 {item['fact']}\n\n"
            f"{cta}\n\n"
            f"{hashtag}"
        )

    return text


def make_content():

    item = choose_unused_content()

    content_type = random.choice([
        "text",
        "image",
        "reel"
    ])

    return {
        "content_id": item["id"],
        "category": item["category"],
        "title": item["title"],
        "emoji": item["emoji"],
        "fact": item["fact"],
        "question": item["question"],
        "answer": item["answer"],
        "content_type": content_type,
        "text": make_text_post(item)
    }


def remember(content):

    history = load_json(HISTORY_FILE)

    history.append({
        "content_id": content["content_id"],
        "category": content["category"],
        "title": content["title"],
        "content_type": content["content_type"],
        "text": content["text"]
    })

    save_json(HISTORY_FILE, history)
