import json
import random
from pathlib import Path


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CONTENT_FILE = (
    BASE_DIR
    / "data"
    / "content.json"
)

HISTORY_FILE = (
    BASE_DIR
    / "data"
    / "history.json"
)


# =========================================================
# FACEBOOK HOOKS
# =========================================================

HOOKS = [
    "🤯 ඔබ මේක දැනගෙන හිටියාද?",
    "😱 මේක ඇත්ත කියලා විශ්වාස කරන්නත් අමාරුයි!",
    "👀 මේ ගැන බොහෝ දෙනෙක් දන්නේ නැහැ!",
    "🧠 අද දැනගන්න වටිනා දෙයක් මෙන්න!",
    "✨ ලෝකය ඇත්තටම පුදුමයි!",
    "😲 මේ තොරතුර ඔබව පුදුම කරයි!",
    "💡 අද අපි දැනගන්න යන්නේ පුදුම දෙයක්!",
    "🌍 අපේ ලෝකය ගැන තවත් පුදුම තොරතුරක්!",
    "🔎 මේ ගැන ඔබ කලින් අහලා තිබුණාද?",
    "🤔 පොඩ්ඩක් හිතලා බලන්න..."
]


# =========================================================
# CALL TO ACTIONS
# =========================================================

CTAS = [
    "👇 ඔබ මේක කලින් දැනගෙන හිටියාද? Comment කරන්න!",
    "❤️ මේ වගේ තවත් දේවල් සඳහා අපිව Follow කරන්න!",
    "🔄 මේක ඔබේ යාළුවන්ටත් Share කරන්න!",
    "🤯 පුදුම හිතුණා නම් ❤️ එකක් දාන්න!",
    "👇 ඔබේ අදහස Comment කරන්න!",
    "📲 මේ post එක ඔබේ යාළුවන්ටත් යවන්න!",
    "💬 ඔබ දන්න තවත් දෙයක් තියෙනවා නම් Comment කරන්න!"
]


# =========================================================
# HASHTAGS
# =========================================================

HASHTAGS = [
    "#අරුමපුදුමලෝකය #AmazingFacts",
    "#අරුමපුදුමලෝකය #SinhalaFacts",
    "#අරුමපුදුමලෝකය #දැනගමු",
    "#AmazingWorld #Sinhala",
    "#අරුමපුදුමලෝකය #ලෝකය"
]


# =========================================================
# POST FORMATS
# =========================================================

POST_FORMATS = [
    "fact",
    "question",
    "quiz"
]


# =========================================================
# LOAD JSON
# =========================================================

def load_json(path):

    if not path.exists():

        return []

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):

                return data

            return []

    except json.JSONDecodeError:

        print(
            f"WARNING: Invalid JSON file: {path}"
        )

        return []


# =========================================================
# SAVE JSON
# =========================================================

def save_json(path, data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )


# =========================================================
# GET USED CONTENT
# =========================================================

def get_used_content_ids():

    history = load_json(
        HISTORY_FILE
    )

    used = set()

    for item in history:

        if not isinstance(item, dict):
            continue

        content_id = item.get(
            "content_id"
        )

        if content_id:

            used.add(content_id)

    return used


# =========================================================
# CHOOSE NEW CONTENT
# =========================================================

def choose_unused_content():

    content = load_json(
        CONTENT_FILE
    )

    if not content:

        raise RuntimeError(
            "data/content.json is empty."
        )

    used = get_used_content_ids()

    available = []

    for item in content:

        if not isinstance(item, dict):
            continue

        content_id = item.get("id")

        if not content_id:
            continue

        if content_id not in used:

            available.append(item)

    if not available:

        raise RuntimeError(
            "NO UNUSED CONTENT REMAINS.\n\n"
            "All content in data/content.json "
            "has already been used."
        )

    return random.choice(
        available
    )


# =========================================================
# MAKE FACT POST
# =========================================================

def make_fact_post(item):

    hook = random.choice(
        HOOKS
    )

    cta = random.choice(
        CTAS
    )

    hashtag = random.choice(
        HASHTAGS
    )

    return (
        f"{hook}\n\n"
        f"{item['emoji']} {item['title']}\n\n"
        f"💡 {item['fact']}\n\n"
        f"{cta}\n\n"
        f"{hashtag}"
    )


# =========================================================
# MAKE QUESTION POST
# =========================================================

def make_question_post(item):

    cta = random.choice(
        CTAS
    )

    hashtag = random.choice(
        HASHTAGS
    )

    return (
        f"🤔 {item['emoji']} "
        f"{item['title']}\n\n"
        f"{item['question']}\n\n"
        f"💬 ඔබේ පිළිතුර "
        f"Comment කරන්න!\n\n"
        f"{cta}\n\n"
        f"{hashtag}"
    )


# =========================================================
# MAKE QUIZ POST
# =========================================================

def make_quiz_post(item):

    hashtag = random.choice(
        HASHTAGS
    )

    return (
        f"🧩 පොඩි Quiz එකක්!\n\n"
        f"{item['emoji']} "
        f"{item['title']}\n\n"
        f"{item['question']}\n\n"
        f"👇 ඔබේ පිළිතුර "
        f"Comment කරන්න!\n\n"
        f"💡 නිවැරදි පිළිතුර: "
        f"{item['answer']}\n\n"
        f"🔄 මේක ඔබේ යාළුවන්ටත් "
        f"Share කරන්න!\n\n"
        f"{hashtag}"
    )


# =========================================================
# CREATE FACEBOOK CAPTION
# =========================================================

def make_facebook_caption(item):

    post_format = random.choice(
        POST_FORMATS
    )

    if post_format == "question":

        text = make_question_post(
            item
        )

    elif post_format == "quiz":

        text = make_quiz_post(
            item
        )

    else:

        text = make_fact_post(
            item
        )

    return text


# =========================================================
# CHOOSE MEDIA TYPE
#
# IMPORTANT:
# THERE ARE NO TEXT-ONLY POSTS.
#
# Image = 75%
# Reel  = 25%
# =========================================================

def choose_media_type():

    media_types = [
        "image",
        "image",
        "image",
        "reel"
    ]

    return random.choice(
        media_types
    )


# =========================================================
# CREATE COMPLETE CONTENT
# =========================================================

def make_content():

    item = choose_unused_content()

    media_type = choose_media_type()

    caption = make_facebook_caption(
        item
    )

    content = {

        # ---------------------------------
        # Identity
        # ---------------------------------

        "content_id": item["id"],

        "category": item.get(
            "category",
            "general"
        ),

        "visual": item.get(
            "visual",
            item.get(
                "category",
                "general"
            )
        ),

        "title": item["title"],

        "emoji": item.get(
            "emoji",
            "🌍"
        ),

        # ---------------------------------
        # Actual information
        # ---------------------------------

        "fact": item["fact"],

        "question": item.get(
            "question",
            ""
        ),

        "answer": item.get(
            "answer",
            ""
        ),

        # ---------------------------------
        # Media
        # ---------------------------------

        "content_type": media_type,

        # ---------------------------------
        # Facebook caption
        # ---------------------------------

        "text": caption
    }

    return content


# =========================================================
# SAVE SUCCESSFULLY PUBLISHED CONTENT
# =========================================================

def remember(content):

    history = load_json(
        HISTORY_FILE
    )

    history.append({

        "content_id": content[
            "content_id"
        ],

        "category": content[
            "category"
        ],

        "visual": content.get(
            "visual",
            ""
        ),

        "title": content[
            "title"
        ],

        "content_type": content[
            "content_type"
        ],

        "text": content[
            "text"
        ]
    })

    save_json(
        HISTORY_FILE,
        history
    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print()
    print(
        "===================================="
    )
    print(
        "LOCAL CONTENT ENGINE TEST"
    )
    print(
        "===================================="
    )
    print()

    content = make_content()

    print(
        "Content ID:",
        content["content_id"]
    )

    print(
        "Category:",
        content["category"]
    )

    print(
        "Visual:",
        content["visual"]
    )

    print(
        "Content type:",
        content["content_type"]
    )

    print()
    print(
        "Facebook caption:"
    )
    print()
    print(
        content["text"]
    )
    print()

    print(
        "===================================="
    )
