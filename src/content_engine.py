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
    "👇 ඔබ මේක කලින් දැනගෙන හිටියාද? Comment කරන්න!",
    "🔄 මේක ඔබේ යාළුවන්ටත් Share කරන්න!",
    "🤯 පුදුම හිතුණා නම් ❤️ එකක් දාන්න!",
    "🌍 තවත් අලුත් දේවල් දැනගන්න අපිත් එක්ක එකතු වෙන්න!"
]


HASHTAGS = [
    "#අරුමපුදුමලෝකය #AmazingFacts #SinhalaFacts",
    "#අරුමපුදුමලෝකය #දැනගමු #InterestingFacts",
    "#අරුමපුදුමලෝකය #Sinhala #Facts",
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


def already_used(title, history):
    current = normalize(title)

    for item in history:
        previous = normalize(
            item.get("source_title", "")
        )

        if current == previous:
            return True

    return False


def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    # Remove common unwanted wiki remnants.
    unwanted = [
        "{{",
        "}}",
        "[[",
        "]]",
        "==",
        "'''",
        "''"
    ]

    for item in unwanted:
        text = text.replace(item, "")

    return text.strip()


def make_post(source):

    hooks = load_json(HOOKS_FILE)
    formats = load_json(FORMATS_FILE)

    hook = random.choice(hooks)
    content_format = random.choice(formats)
    cta = random.choice(CTAS)
    hashtag = random.choice(HASHTAGS)

    title = source["title"]
    paragraph = clean_text(source["source"])

    # Keep Facebook posts readable.
    if len(paragraph) > 650:
        paragraph = (
            paragraph[:650]
            .rsplit(" ", 1)[0]
            + "..."
        )

    if content_format == "question":

        message = (
            f"🤔 {title}\n\n"
            f"{paragraph}\n\n"
            f"💬 මේ ගැන ඔබේ අදහස මොකක්ද?"
        )

    elif content_format == "quiz":

        message = (
            f"🧩 පොඩි Quiz එකක්!\n\n"
            f"📚 මාතෘකාව: {title}\n\n"
            f"{paragraph}\n\n"
            f"👇 ඔබේ පිළිතුර Comment කරන්න!"
        )

    elif content_format == "challenge":

        message = (
            f"🧠 ඔබ මේක දැනගෙන හිටියාද?\n\n"
            f"🔎 {title}\n\n"
            f"{paragraph}"
        )

    elif content_format == "comparison":

        message = (
            f"⚖️ අද දැනගමු!\n\n"
            f"🌍 {title}\n\n"
            f"{paragraph}"
        )

    else:

        message = (
            f"{hook}\n\n"
            f"💡 {title}\n\n"
            f"{paragraph}"
        )

    message += (
        f"\n\n{cta}"
        f"\n\n{hashtag}"
    )

    return {
        "id": (
            "wiki_"
            + normalize(title)
            .replace(" ", "_")
        ),
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

    # Try several different fresh sources.
    for _ in range(15):

        source = get_fresh_source()

        if not source:
            continue

        if already_used(
            source["title"],
            history
        ):
            continue

        post = make_post(source)

        if post:
            return post

    # Local database fallback.
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

    if available:

        fact = random.choice(available)
        cta = random.choice(CTAS)
        hashtag = random.choice(HASHTAGS)

        return {
            "id": fact["id"],
            "category": fact.get(
                "category",
                "unknown"
            ),
            "topic": fact.get(
                "topic",
                "unknown"
            ),
            "format": "fact",
            "hook": "🤯 ඔබ මේක දැනගෙන හිටියාද?",
            "cta": cta,
            "fact": fact["fact"],
            "source_title": "",
            "source_url": "",
            "text": (
                "🤯 ඔබ මේක දැනගෙන හිටියාද?\n\n"
                f"💡 {fact['fact']}\n\n"
                f"{cta}\n\n"
                f"{hashtag}"
            )
        }

    raise RuntimeError(
        "No new content is available."
    )


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
            "source_title",
            ""
        ),
        "source_url": content.get(
            "source_url",
            ""
        ),
        "text": content["text"]
    })

    save_json(
        HISTORY_FILE,
        history
    )
