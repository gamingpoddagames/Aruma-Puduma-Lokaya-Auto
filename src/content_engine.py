import json
import random
import re
from pathlib import Path

from src.fresh_source import get_fresh_source


BASE_DIR = Path(__file__).resolve().parent.parent

FACTS_FILE = BASE_DIR / "data" / "facts.json"
HISTORY_FILE = BASE_DIR / "data" / "history.json"
HOOKS_FILE = BASE_DIR / "data" / "hooks.json"
FORMATS_FILE = BASE_DIR / "data" / "formats.json"


CTAS = [
    "❤️ මේ වගේ තවත් පුදුම දේවල් දැනගන්න අපිව Follow කරන්න!",
    "👇 මේ ගැන ඔබ කලින් දැනගෙන හිටියාද? Comment කරන්න!",
    "🔄 මේක ඔබේ යාළුවන්ටත් Share කරන්න!",
    "🤯 පුදුම හිතුණා නම් ❤️ එකක් දාන්න!",
    "🌍 තවත් අලුත් Facts සඳහා අපිත් එක්ක එකතු වෙන්න!"
]


HASHTAGS = [
    "#අරුමපුදුමලෝකය #AmazingFacts #SinhalaFacts",
    "#අරුමපුදුමලෝකය #දැනගමු #InterestingFacts",
    "#AmazingWorld #Sinhala #Facts",
    "#අරුමපුදුමලෝකය #DidYouKnow"
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


def normalize(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def already_used(source_title, history):
    title = normalize(source_title)

    for item in history:
        old_title = normalize(
            item.get("source_title", "")
        )

        if old_title == title:
            return True

    return False


def make_source_post(source):
    hooks = load_json(HOOKS_FILE)
    formats = load_json(FORMATS_FILE)

    hook = random.choice(hooks)
    content_format = random.choice(formats)
    cta = random.choice(CTAS)
    hashtag = random.choice(HASHTAGS)

    title = source["title"]
    source_text = source["source"]

    # Use the first useful paragraph.
    paragraphs = [
        p.strip()
        for p in source_text.split("\n")
        if len(p.strip()) > 80
    ]

    if not paragraphs:
        return None

    paragraph = paragraphs[0]

    # Keep Facebook post reasonably short.
    if len(paragraph) > 500:
        paragraph = paragraph[:500].rsplit(" ", 1)[0] + "..."

    if content_format == "question":
        message = (
            f"{hook}\n\n"
            f"🌍 {title}\n\n"
            f"{paragraph}\n\n"
            f"🤔 මේ ගැන ඔබේ අදහස මොකක්ද?"
        )

    elif content_format == "quiz":
        message = (
            f"{hook}\n\n"
            f"🧩 පොඩි Quiz එකක්!\n\n"
            f"📚 මාතෘකාව: {title}\n\n"
            f"{paragraph}\n\n"
            f"👇 ඔබ දන්නා දේ Comment කරන්න!"
        )

    elif content_format == "challenge":
        message = (
            f"{hook}\n\n"
            f"🧠 Challenge එකක්!\n\n"
            f"{title} ගැන මේ තොරතුර කියවලා "
            f"ඔබේ යාළුවෙකුටත් කියන්න:\n\n"
            f"{paragraph}"
        )

    elif content_format == "comparison":
        message = (
            f"{hook}\n\n"
            f"🌍 {title}\n\n"
            f"{paragraph}\n\n"
            f"✨ මේ වගේ තවත් පුදුම දේවල් බලමු!"
        )

    else:
        message = (
            f"{hook}\n\n"
            f"💡 {title}\n\n"
            f"{paragraph}"
        )

    message += f"\n\n{cta}\n\n{hashtag}"

    return {
        "id": "wiki_" + normalize(title).replace(" ", "_"),
        "category": "fresh_source",
        "topic": title,
        "format": content_format,
        "hook": hook,
        "cta": cta,
        "fact": paragraph,
        "source_title": title,
        "source_url": source["url"],
        "text": message
    }


def choose_content():

    history = load_json(HISTORY_FILE)

    # Try several fresh sources.
    for _ in range(10):

        source = get_fresh_source()

        if not source:
            continue

        if already_used(source["title"], history):
            continue

        post = make_source_post(source)

        if post:
            return post

    # Fall back to an unused local fact.
    facts = load_json(FACTS_FILE)

    used_ids = {
        item.get("id")
        for item in history
        if isinstance(item, dict)
    }

    available = [
        fact
        for fact in facts
        if fact.get("id") not in used_ids
    ]

    if not available:
        raise RuntimeError(
            "No new source-backed content or local facts available."
        )

    fact = random.choice(available)

    return {
        "id": fact["id"],
        "category": fact.get("category", "unknown"),
        "topic": fact.get("topic", "unknown"),
        "format": "fact",
        "hook": "🤯 ඔබ මේක දැනගෙන හිටියද?",
        "cta": random.choice(CTAS),
        "fact": fact["fact"],
        "source_title": "",
        "source_url": "",
        "text": (
            f"🤯 ඔබ මේක දැනගෙන හිටියද?\n\n"
            f"💡 {fact['fact']}\n\n"
            f"{random.choice(CTAS)}\n\n"
            f"{random.choice(HASHTAGS)}"
        )
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
        "source_title": content.get(
            "source_title", ""
        ),
        "source_url": content.get(
            "source_url", ""
        ),
        "text": content["text"]
    })

    save_json(HISTORY_FILE, history)
