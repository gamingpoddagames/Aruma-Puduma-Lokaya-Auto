import random
import requests
from urllib.parse import quote

WIKIPEDIA_API = "https://en.wikipedia.org/w/rest.php/v1"

TOPICS = [
    "animals",
    "space",
    "science",
    "ocean",
    "human body",
    "nature",
    "technology",
    "history",
    "ancient world",
    "geography",
    "Sri Lanka",
    "astronomy",
    "inventions",
    "architecture",
    "transportation",
    "psychology",
    "Earth",
    "weather",
    "plants",
    "dinosaurs"
]

USER_AGENT = (
    "ArumaPudumaLokayaAuto/1.0 "
    "(Facebook content project)"
)


def search_wikipedia(query, limit=10):
    url = f"{WIKIPEDIA_API}/search/page"

    response = requests.get(
        url,
        params={
            "q": query,
            "limit": limit
        },
        headers={
            "User-Agent": USER_AGENT
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()
    return data.get("pages", [])


def get_article(title):
    encoded_title = quote(title.replace(" ", "_"), safe="")

    url = (
        f"{WIKIPEDIA_API}/page/"
        f"{encoded_title}"
    )

    response = requests.get(
        url,
        headers={
            "User-Agent": USER_AGENT
        },
        timeout=30
    )

    if response.status_code != 200:
        return None

    return response.json()


def get_fresh_source():
    topic = random.choice(TOPICS)

    pages = search_wikipedia(topic)

    if not pages:
        return None

    random.shuffle(pages)

    for page in pages:
        title = page.get("title")

        if not title:
            continue

        article = get_article(title)

        if not article:
            continue

        source_text = article.get("source", "").strip()

        if len(source_text) < 150:
            continue

        return {
            "title": title,
            "source": source_text,
            "url": (
                "https://en.wikipedia.org/wiki/"
                + quote(title.replace(" ", "_"))
            ),
            "topic": topic
        }

    return None
