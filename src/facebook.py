import os
import time
from pathlib import Path

import requests


# ============================================================
# FACEBOOK SETTINGS
# ============================================================

GRAPH_VERSION = "v23.0"
GRAPH_URL = f"https://graph.facebook.com/{GRAPH_VERSION}"

PAGE_ID = os.getenv("FB_PAGE_ID")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")


# ============================================================
# CHECK FACEBOOK SETTINGS
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
# FACEBOOK ERROR HANDLER
# ============================================================

def facebook_error(response, message):
    try:
        data = response.json()
    except Exception:
        data = response.text

    raise RuntimeError(
        f"{message} {response.status_code}: {data}"
    )


# ============================================================
# TEXT POST
# ============================================================

def publish_text_post(text):

    check_credentials()

    url = f"{GRAPH_URL}/{PAGE_ID}/feed"

    data = {
        "message": text,
        "access_token": PAGE_ACCESS_TOKEN
    }

    print("")
    print("====================================")
    print("PUBLISHING FACEBOOK TEXT POST")
    print("====================================")

    response = requests.post(
        url,
        data=data,
        timeout=120
    )

    if not response.ok:
        facebook_error(
            response,
            "Facebook text post error:"
        )

    result = response.json()

    print("Facebook response:")
    print(result)

    print("Text post successfully published.")

    return result


# ============================================================
# IMAGE POST
# ============================================================

def publish_image_post(
    image_path,
    caption
):

    check_credentials()

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    print("")
    print("====================================")
    print("PUBLISHING FACEBOOK IMAGE POST")
    print("====================================")

    print(
        f"Image: {image_path}"
    )

    url = f"{GRAPH_URL}/{PAGE_ID}/photos"

    with image_path.open("rb") as image_file:

        files = {
            "source": (
                image_path.name,
                image_file,
                "image/png"
            )
        }

        data = {
            "message": caption,
            "access_token": PAGE_ACCESS_TOKEN
        }

        response = requests.post(
            url,
            data=data,
            files=files,
            timeout=300
        )

    if not response.ok:
        facebook_error(
            response,
            "Facebook image post error:"
        )

    result = response.json()

    print("Facebook image response:")
    print(result)

    print("Image post successfully published.")

    return result


# ============================================================
# START REEL UPLOAD
# ============================================================

def start_reel_upload():

    check_credentials()

    url = f"{GRAPH_URL}/{PAGE_ID}/video_reels"

    data = {
        "upload_phase": "start",
        "access_token": PAGE_ACCESS_TOKEN
    }

    print("")
    print("Starting Facebook Reel upload...")

    response = requests.post(
        url,
        data=data,
        timeout=120
    )

    if not response.ok:
        facebook_error(
            response,
            "Facebook Reel START error:"
        )

    result = response.json()

    print("START response:")
    print(result)

    if "video_id" not in result:
        raise RuntimeError(
            "Facebook did not return video_id.\n"
            + str(result)
        )

    if "upload_url" not in result:
        raise RuntimeError(
            "Facebook did not return upload_url.\n"
            + str(result)
        )

    return result


# ============================================================
# UPLOAD REEL VIDEO FILE
# ============================================================

def upload_reel_binary(
    upload_url,
    video_path
):

    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(
            f"Reel video not found: {video_path}"
        )

    file_size = video_path.stat().st_size

    print("")
    print("====================================")
    print("UPLOADING REEL VIDEO FILE")
    print("====================================")

    print(
        f"File: {video_path}"
    )

    print(
        f"Size: {file_size:,} bytes"
    )

    # Facebook Reel upload requires
    # the actual MP4 binary data.

    headers = {
        "Authorization":
            f"OAuth {PAGE_ACCESS_TOKEN}",

        "offset":
            "0",

        "file_size":
            str(file_size),

        "Content-Type":
            "application/octet-stream"
    }

    with video_path.open("rb") as video_file:

        response = requests.post(
            upload_url,
            headers=headers,
            data=video_file,
            timeout=900
        )

    if not response.ok:
        facebook_error(
            response,
            "Facebook Reel binary upload error:"
        )

    try:
        result = response.json()
    except Exception:
        result = {
            "success": True,
            "raw": response.text
        }

    print("")
    print("Facebook binary upload response:")
    print(result)

    if result.get("success") is False:

        raise RuntimeError(
            "Facebook reported that the video upload failed:\n"
            + str(result)
        )

    print(
        "Reel video uploaded successfully."
    )

    return result


# ============================================================
# CHECK REEL STATUS
# ============================================================

def check_reel_status(video_id):

    url = f"{GRAPH_URL}/{video_id}"

    params = {
        "fields": "status",
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.get(
        url,
        params=params,
        timeout=120
    )

    if not response.ok:
        facebook_error(
            response,
            "Facebook Reel status error:"
        )

    result = response.json()

    print("")
    print("Reel processing status:")
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

    url = f"{GRAPH_URL}/{PAGE_ID}/video_reels"

    data = {
        "video_id": video_id,
        "upload_phase": "finish",
        "video_state": "PUBLISHED",
        "description": description,
        "access_token": PAGE_ACCESS_TOKEN
    }

    if title:
        data["title"] = title

    print("")
    print("====================================")
    print("PUBLISHING REEL")
    print("====================================")

    response = requests.post(
        url,
        data=data,
        timeout=300
    )

    if not response.ok:
        facebook_error(
            response,
            "Facebook Reel FINISH error:"
        )

    result = response.json()

    print("")
    print("Facebook Reel publish response:")
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

    video_path = Path(video_path)

    if not video_path.exists():

        raise FileNotFoundError(
            f"Reel does not exist:\n{video_path}"
        )

    print("")
    print("====================================")
    print("FACEBOOK REEL PUBLISHING")
    print("====================================")

    print(
        f"Video: {video_path}"
    )

    print(
        f"Size: {video_path.stat().st_size:,} bytes"
    )

    # --------------------------------------------------------
    # STEP 1
    # START
    # --------------------------------------------------------

    start = start_reel_upload()

    video_id = start["video_id"]
    upload_url = start["upload_url"]

    print("")
    print(
        f"Facebook Video ID: {video_id}"
    )

    # --------------------------------------------------------
    # STEP 2
    # UPLOAD ACTUAL MP4
    # --------------------------------------------------------

    upload_result = upload_reel_binary(
        upload_url,
        video_path
    )

    print("")
    print(
        "Binary upload completed."
    )

    print(
        upload_result
    )

    # --------------------------------------------------------
    # STEP 3
    # WAIT FOR FACEBOOK
    # --------------------------------------------------------

    print("")
    print(
        "Waiting for Facebook to process Reel..."
    )

    for attempt in range(6):

        time.sleep(5)

        try:

            status = check_reel_status(
                video_id
            )

            print(
                f"Processing check "
                f"{attempt + 1}/6"
            )

            print(status)

        except Exception as error:

            print(
                "Status check warning:"
            )

            print(error)

    # --------------------------------------------------------
    # STEP 4
    # FINISH / PUBLISH
    # --------------------------------------------------------

    result = finish_reel_upload(
        video_id,
        description,
        title
    )

    print("")
    print("====================================")
    print("FACEBOOK REEL PUBLISHED")
    print("====================================")

    print(result)

    return result


# ============================================================
# OPTIONAL ALIAS
# ============================================================
#
# If any old code uses publish_photo(),
# it will still work.
#

def publish_photo(
    image_path,
    caption
):

    return publish_image_post(
        image_path,
        caption
    )
