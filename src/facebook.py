import os
import requests


GRAPH_API_VERSION = "v23.0"


def publish_text_post(message):
    page_id = os.environ.get("FB_PAGE_ID")
    page_access_token = os.environ.get("FB_PAGE_ACCESS_TOKEN")

    if not page_id:
        raise RuntimeError("FB_PAGE_ID GitHub Secret is missing.")

    if not page_access_token:
        raise RuntimeError("FB_PAGE_ACCESS_TOKEN GitHub Secret is missing.")

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/feed"

    response = requests.post(
        url,
        data={
            "message": message,
            "access_token": page_access_token
        },
        timeout=60
    )

    if not response.ok:
        raise RuntimeError(
            f"Facebook API error {response.status_code}: "
            f"{response.text}"
        )

    return response.json()
