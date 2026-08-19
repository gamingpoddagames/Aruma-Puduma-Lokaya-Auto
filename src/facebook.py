import os
import time
from pathlib import Path

import requests


# ============================================================
# SETTINGS
# ============================================================

GRAPH_VERSION = "v23.0"

GRAPH_URL = f"https://graph.facebook.com/{GRAPH_VERSION}"


# ============================================================
# ENVIRONMENT
# ============================================================

PAGE_ID = os.getenv("FB_PAGE_ID")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")


# ============================================================
# CHECK SETTINGS
# ============================================================

def check_credentials():

    if not PAGE_ID:
        raise RuntimeError(
            "FB_PAGE_ID GitHub Secret is missing."
        )

    if not PAGE_ACCESS_TOKEN:
        raise RuntimeError(
            "FB_PAGE_ACCESS_TOKEN GitHub Secret is missing."
        )


# ============================================================
# FACEBOOK API ERROR
# ============================================================

def raise_facebook_error(response, title):

    try:
        data = response.json()
    except Exception:
        data = response.text

    raise RuntimeError(
        f"{title} {response.status_code}: {data}"
    )


# ============================================================
# TEXT POST
# ============================================================

def publish_text_post(text):

    check_credentials()

    url = (
        f"{GRAPH_URL}/{PAGE_ID}/feed"
    )

    payload = {
        "message": text,
        "access_token": PAGE_ACCESS_TOKEN,
    }

    print(
        "Publishing Facebook text post..."
    )

    response = requests.post(
        url,
        data=payload,
        timeout=60
    )

    if not response.ok:
        raise_facebook_error(
            response,
            "Facebook API error"
        )

    result = response.json()

    print(
        "Facebook response:"
    )

    print(result)

    return result


# ============================================================
# PHOTO POST
# ============================================================

def publish_photo(
    image_path,
    caption
):

    check_credentials()

    image_path = Path(
        image_path
    )

    if not image_path.exists():

        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    url = (
        f"{GRAPH_URL}/{PAGE_ID}/photos"
    )

    print(
        "Publishing Facebook image post..."
    )

    with image_path.open(
        "rb"
    ) as image_file:

        files = {
            "source": (
                image_path.name,
                image_file,
                "image/png"
            )
        }

        data = {
            "message": caption,
            "access_token":
                PAGE_ACCESS_TOKEN,
        }

        response = requests.post(
            url,
            data=data,
            files=files,
            timeout=120
        )

    if not response.ok:
        raise_facebook_error(
            response,
            "Facebook image error"
        )

    result = response.json()

    print(
        "Facebook image response:"
    )

    print(result)

    return result


# ============================================================
# START REEL UPLOAD
# ============================================================

def start_reel_upload():

    check_credentials()

    url = (
        f"{GRAPH_URL}/{PAGE_ID}/video_reels"
    )

    data = {
        "upload_phase": "start",
        "access_token":
            PAGE_ACCESS_TOKEN,
    }

    print(
        "Starting Facebook Reel upload..."
    )

    response = requests.post(
        url,
        data=data,
        timeout=60
    )

    if not response.ok:
        raise_facebook_error(
            response,
            "Facebook Reel START error"
        )

    result = response.json()

    if "video_id" not in result:
        raise RuntimeError(
            "Facebook did not return video_id: "
            + str(result)
        )

    if "upload_url" not in result:
        raise RuntimeError(
            "Facebook did not return upload_url: "
            + str(result)
        )

    print(
        "Facebook Reel upload session:"
    )

    print(result)

    return result


# ============================================================
# UPLOAD REEL BINARY
# ============================================================

def upload_reel_binary(
    upload_url,
    video_path
):

    video_path = Path(
        video_path
    )

    if not video_path.exists():

        raise FileNotFoundError(
            f"Reel file not found: {video_path}"
        )

    file_size = (
        video_path.stat().st_size
    )

    print(
        f"Uploading Reel file: "
        f"{file_size:,} bytes"
    )

    headers = {
        "Authorization":
            f"OAuth {PAGE_ACCESS_TOKEN}",

        "offset":
            "0",

        "file_size":
            str(file_size),

        "Content-Type":
            "application/octet-stream",
    }

    # IMPORTANT:
    # Facebook expects the actual binary
    # video data here.

    with video_path.open(
        "rb"
    ) as video_file:

        response = requests.post(
            upload_url,
            headers=headers,
            data=video_file,
            timeout=600
        )

    if not response.ok:
        raise_facebook_error(
            response,
            "Facebook Reel binary upload error"
        )

    try:
        result = response.json()
    except Exception:
        result = {
            "success": True,
            "raw": response.text
        }

    print(
        "Facebook Reel upload response:"
    )

    print(result)

    if result.get(
        "success"
    ) is False:

        raise RuntimeError(
            "Facebook reported Reel upload failure: "
            + str(result)
        )

    return result


# ============================================================
# CHECK REEL STATUS
# ============================================================

def check_reel_status(
    video_id
):

    url = (
        f"{GRAPH_URL}/{video_id}"
    )

    params = {
        "fields": "status",
        "access_token":
            PAGE_ACCESS_TOKEN,
    }

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    if not response.ok:
        raise_facebook_error(
            response,
            "Facebook Reel status error"
        )

    result = response.json()

    print(
        "Reel processing status:"
    )

    print(result)

    return result


# ============================================================
# FINISH / PUBLISH REEL
# ============================================================

def finish_reel_upload(
    video_id,
    description,
    title=""
):

    check_credentials()

    url = (
        f"{GRAPH_URL}/{PAGE_ID}/video_reels"
    )

    data = {
        "video_id": video_id,

        "upload_phase": "finish",

        "video_state": "PUBLISHED",

        "description": description,

        "access_token":
            PAGE_ACCESS_TOKEN,
    }

    if title:
        data["title"] = title

    print(
        "Publishing Reel on Facebook..."
    )

    response = requests.post(
        url,
        data=data,
        timeout=120
    )

    if not response.ok:
        raise_facebook_error(
            response,
            "Facebook Reel FINISH error"
        )

    result = response.json()

    print(
        "Facebook Reel publish response:"
    )

    print(result)

    return result


# ============================================================
# COMPLETE REEL PUBLISHING
# ============================================================

def publish_reel(
    video_path,
    description,
    title=""
):

    check_credentials()

    video_path = Path(
        video_path
    )

    if not video_path.exists():

        raise FileNotFoundError(
            f"Reel does not exist: {video_path}"
        )

    print("")
    print(
        "===================================="
    )
    print(
        "FACEBOOK REEL UPLOAD"
    )
    print(
        "===================================="
    )

    # --------------------------------------------------------
    # STEP 1
    # --------------------------------------------------------

    start_result = start_reel_upload()

    video_id = start_result[
        "video_id"
    ]

    upload_url = start_result[
        "upload_url"
    ]

    print(
        f"Video ID: {video_id}"
    )

    print(
        f"Upload URL: {upload_url}"
    )

    # --------------------------------------------------------
    # STEP 2
    # --------------------------------------------------------

    upload_result = upload_reel_binary(
        upload_url,
        video_path
    )

    print(
        "Reel binary uploaded successfully."
    )

    # --------------------------------------------------------
    # STEP 3
    # --------------------------------------------------------

    print(
        "Checking Reel processing..."
    )

    # Facebook can process asynchronously.
    # Give it a short amount of time before FINISH.

    for attempt in range(5):

        time.sleep(5)

        try:

            status = check_reel_status(
                video_id
            )

            print(
                f"Processing check "
                f"{attempt + 1}/5"
            )

            print(status)

        except Exception as error:

            print(
                "Status check warning:",
                error
            )

    # --------------------------------------------------------
    # STEP 4
    # --------------------------------------------------------

    result = finish_reel_upload(
        video_id,
        description,
        title
    )

    print(
        ""
    )

    print(
        "===================================="
    )

    print(
        "REEL SUCCESSFULLY SENT TO FACEBOOK"
    )

    print(
        "===================================="
    )

    return result
