import random
import requests
from urllib.parse import quote

WIKIPEDIA_API = "https://si.wikipedia.org/w/api.php"

USER_AGENT = (
    "ArumaPudumaLokayaAuto/1.0 "
    "(automated Sinhala educational Facebook page)"
)

TOPICS = [
    "සතුන්",
    "අභ්‍යවකාශය",
    "විද්‍යාව",
    "සාගරය",
    "ස්වභාවධර්මය",
    "තාක්ෂණය",
    "ඉතිහාසය",
    "පුරාණ ලෝකය",
    "භූගෝල විද්‍යාව",
    "ශ්‍රී ලංකාව",
    "තාරකා විද්‍යාව",
    "නව නිපැයුම්",
    "ගෘහ නිර්මාණ ශිල්පය",
    "වාහන",
    "ගුවන් යානා",
    "පෘථිවිය",
    "කාලගුණය",
    "ශාක",
    "ඩයිනෝසර්",
    "මුහුදු සතුන්"
]


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
        headers={
            "User-Agent": USER_AGENT
        },
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
            "exsentences": "4",
            "exlimit": "1",
            "titles": title,
            "format": "json",
            "formatversion": "2"
        },
        headers={
            "User-Agent": USER_AGENT
        },
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

        results = search_wikipedia(
            topic,
            limit=10
        )

        if not results:
            continue

        random.shuffle(results)

        for result in results:

            title = result.get("title")

            if not title:
                continue

            extract = get_plaintext_extract(title)

            if not extract:
                continue

            # Don't use list/index/disambiguation pages.
            bad_words = [
                "වර්ගීකරණය",
                "බහුවිධ අර්ථ",
                "ලැයිස්තුව",
                "ප්‍රවර්ගය"
            ]

            lower_title = title.lower()

            if any(
                word.lower() in lower_title
                for word in bad_words
            ):
                continue

            return {
                "title": title,
                "source": extract,
                "url": (
                    "https://si.wikipedia.org/wiki/"
                    + quote(title.replace(" ", "_"))
                ),
                "topic": topic
            }

    return None
