import os
import requests


GRAPH_URL = "https://graph.facebook.com/v23.0"


def get_credentials():
    page_id = os.getenv("FB_PAGE_ID")
    access_token = os.getenv("FB_PAGE_ACCESS_TOKEN")

    if not page_id:
        raise RuntimeError("FB_PAGE_ID GitHub Secret is missing.")

    if not access_token:
        raise RuntimeError(
            "FB_PAGE_ACCESS_TOKEN GitHub Secret is missing."
        )

    return page_id, access_token


def publish_text_post(text):

    page_id, access_token = get_credentials()

    url = f"{GRAPH_URL}/{page_id}/feed"

    response = requests.post(
        url,
        data={
            "message": text,
            "access_token": access_token
        },
        timeout=60
    )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Facebook API error {response.status_code}: "
            f"{response.text}"
        )

    return response.json()


def publish_image_post(image_path, caption):

    page_id, access_token = get_credentials()

    url = f"{GRAPH_URL}/{page_id}/photos"

    with open(image_path, "rb") as image_file:

        response = requests.post(
            url,
            files={
                "source": image_file
            },
            data={
                "caption": caption,
                "access_token": access_token
            },
            timeout=120
        )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Facebook image error {response.status_code}: "
            f"{response.text}"
        )

    return response.json()


def publish_reel(video_path, description):

    page_id, access_token = get_credentials()

    # Step 1: initialize Reel upload.
    upload_url = (
        f"{GRAPH_URL}/{page_id}/video_reels"
    )

    response = requests.post(
        upload_url,
        data={
            "upload_phase": "start",
            "access_token": access_token
        },
        timeout=60
    )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Facebook Reel initialization error "
            f"{response.status_code}: {response.text}"
        )

    start_data = response.json()

    video_id = start_data.get("video_id")

    if not video_id:
        raise RuntimeError(
            f"Facebook did not return video_id: "
            f"{start_data}"
        )

    # Step 2: upload video bytes.
    upload_endpoint = (
        f"{GRAPH_URL}/{video_id}"
    )

    file_size = os.path.getsize(video_path)

    with open(video_path, "rb") as video_file:

        response = requests.post(
            upload_endpoint,
            headers={
                "Authorization":
                    f"OAuth {access_token}",
                "offset": "0",
                "file_size": str(file_size)
            },
            data=video_file,
            timeout=300
        )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Facebook Reel upload error "
            f"{response.status_code}: {response.text}"
        )

    # Step 3: publish Reel.
    publish_response = requests.post(
        upload_url,
        data={
            "upload_phase": "finish",
            "video_id": video_id,
            "video_state": "PUBLISHED",
            "description": description,
            "access_token": access_token
        },
        timeout=120
    )

    if publish_response.status_code >= 400:
        raise RuntimeError(
            f"Facebook Reel publishing error "
            f"{publish_response.status_code}: "
            f"{publish_response.text}"
        )

    return publish_response.json()
