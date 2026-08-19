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
    "ancient world",import random
import requests
from urllib.parse import quote

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

TOPICS = [
    "animals",
    "space",
    "science",
    "ocean",
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
    "dinosaurs",
    "interesting facts"
]

USER_AGENT = (
    "ArumaPudumaLokayaAuto/1.0 "
    "(automated educational Facebook page)"
)


def search_wikipedia(query, limit=10):
    response = requests.get(
        WIKIPEDIA_API,
        params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "format": "json",
            "formatversion": "2"
        },
        headers={"User-Agent": USER_AGENT},
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data.get("query", {}).get("search", [])


def get_plaintext_extract(title):
    response = requests.get(
        WIKIPEDIA_API,
        params={
            "action": "query",
            "prop": "extracts",
            "exintro": "1",
            "explaintext": "1",
            "exsentences": "5",
            "exlimit": "1",
            "titles": title,
            "format": "json",
            "formatversion": "2"
        },
        headers={"User-Agent": USER_AGENT},
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    pages = data.get("query", {}).get("pages", [])

    if not pages:
        return None

    extract = pages[0].get("extract", "").strip()

    if len(extract) < 100:
        return None

    return extract


def get_fresh_source():
    topics = TOPICS.copy()
    random.shuffle(topics)

    for topic in topics:

        pages = search_wikipedia(topic, limit=10)

        if not pages:
            continue

        random.shuffle(pages)

        for page in pages:

            title = page.get("title")

            if not title:
                continue

            # Get clean reader-friendly text.
            extract = get_plaintext_extract(title)

            if not extract:
                continue

            # Reject obvious Wikipedia/system pages.
            blocked = [
                "disambiguation",
                "list of",
                "index of",
                "template:",
                "category:"
            ]

            lower_title = title.lower()

            if any(word in lower_title for word in blocked):
                continue

            return {
                "title": title,
                "source": extract,
                "url": (
                    "https://en.wikipedia.org/wiki/"
                    + quote(title.replace(" ", "_"))
                ),
                "topic": topic
            }

    return None
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
