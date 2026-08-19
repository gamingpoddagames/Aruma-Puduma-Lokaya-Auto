import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FACTS_FILE = BASE_DIR / "data" / "facts.json"
HISTORY_FILE = BASE_DIR / "data" / "history.json"
HOOKS_FILE = BASE_DIR / "data" / "hooks.json"
FORMATS_FILE = BASE_DIR / "data" / "formats.json"


CTAS = [
    "❤️ මේ වගේ තවත් පුදුම Facts සඳහා අපිව Follow කරන්න!",
    "👇 ඔබ මේක කලින් දැනගෙන හිටියාද? Comment කරන්න!",
    "🔄 මේක ඔබේ යාළුවන්ටත් Share කරන්න!",
    "🤯 පුදුම හිතුණා නම් ❤️ එකක් දාන්න!",
    "🌍 තවත් අලුත් දේවල් දැනගන්න අපිත් එක්ක එකතු වෙන්න!"
]


HASHTAG_SETS = [
    "#අරුමපුදුමලෝකය #AmazingFacts #SinhalaFacts",
    "#අරුමපුදුමලෝකය #දැනගමු #Facts",
    "#AmazingWorld #Sinhala #InterestingFacts",
    "#අරුමපුදුමලෝකය #DidYouKnow #SriLanka",
]


def load_json(path):
    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )


def get_unused_facts():
    facts = load_json(FACTS_FILE)
    history = load_json(HISTORY_FILE)

    used_ids = {
        item.get("id")
        for item in history
        if isinstance(item, dict) and item.get("id")
    }

    return [
        fact
        for fact in facts
        if fact.get("id") not in used_ids
    ]


def make_message(fact, content_format, hook, cta, hashtags):

    fact_text = fact["fact"]

    if content_format == "question":
        body = (
            f"{hook}\n\n"
            f"🤔 මේ ගැන ඔබ මොකද හිතන්නේ?\n\n"
            f"{fact_text}"
        )

    elif content_format == "quiz":
        body = (
            f"{hook}\n\n"
            f"🧩 පොඩි Quiz එකක්!\n\n"
            f"{fact_text}\n\n"
            f"👇 ඔබේ පිළිතුර Comment කරන්න!"
        )

    elif content_format == "challenge":
        body = (
            f"{hook}\n\n"
            f"🧠 ඔබට මේක කලින් දැනගෙන හිටියාද?\n\n"
            f"{fact_text}"
        )

    elif content_format == "comparison":
        body = (
            f"{hook}\n\n"
            f"⚖️ මේ ගැන දැනගන්න:\n\n"
            f"{fact_text}"
        )

    elif content_format == "did_you_know":
        body = (
            f"💡 ඔබ දන්නවාද?\n\n"
            f"{fact_text}"
        )

    else:
        body = (
            f"{hook}\n\n"
            f"💡 {fact_text}"
        )

    return f"{body}\n\n{cta}\n\n{hashtags}"


def choose_content():

    unused_facts = get_unused_facts()

    if not unused_facts:
        raise RuntimeError(
            "No unused facts remain. "
            "Add more verified facts before publishing."
        )

    hooks = load_json(HOOKS_FILE)
    formats = load_json(FORMATS_FILE)

    if not hooks:
        raise RuntimeError("hooks.json is empty.")

    if not formats:
        raise RuntimeError("formats.json is empty.")

    fact = random.choice(unused_facts)
    hook = random.choice(hooks)
    content_format = random.choice(formats)
    cta = random.choice(CTAS)
    hashtags = random.choice(HASHTAG_SETS)

    message = make_message(
        fact,
        content_format,
        hook,
        cta,
        hashtags
    )

    return {
        "id": fact["id"],
        "category": fact.get("category", "unknown"),
        "topic": fact.get("topic", "unknown"),
        "format": content_format,
        "hook": hook,
        "fact": fact["fact"],
        "cta": cta,
        "text": message
    }


def remember_content(content):

    history = load_json(HISTORY_FILE)

    history.append({
        "id": content["id"],
        "category": content["category"],
        "topic": content["topic"],
        "format": content["format"],
        "hook": content["hook"],
        "cta": content["cta"],
        "text": content["text"]
    })

    save_json(HISTORY_FILE, history)
