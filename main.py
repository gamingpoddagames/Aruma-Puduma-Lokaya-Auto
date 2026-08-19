from src.local_content_engine import (
    make_content,
    remember
)

from src.media_generator import (
    create_image,
    create_reel
)

from src.facebook import (
    publish_text_post
)


def main():

    content = make_content()

    print()
    print("====================================")
    print("SELECTED CONTENT")
    print("====================================")
    print(content["text"])
    print()
    print("Content type:", content["content_type"])
    print()

    content_type = content["content_type"]

    # -----------------------------
    # TEXT POST
    # -----------------------------

    if content_type == "text":

        print("Publishing Facebook text post...")

        result = publish_text_post(
            content["text"]
        )

        print()
        print("Facebook response:")
        print(result)

    # -----------------------------
    # IMAGE POST
    # -----------------------------

    elif content_type == "image":

        print("Creating Facebook image...")

        image_path = create_image(
            content
        )

        print(
            "Image created:",
            image_path
        )

        # Image publishing will be connected
        # after the image test is confirmed.
        print(
            "Image publishing is not connected yet."
        )

    # -----------------------------
    # REEL
    # -----------------------------

    elif content_type == "reel":

        print("Creating Facebook Reel...")

        reel_path = create_reel(
            content
        )

        print(
            "Reel created:",
            reel_path
        )

        # Reel publishing will be connected
        # after the Reel test is confirmed.
        print(
            "Reel publishing is not connected yet."
        )

    else:

        raise RuntimeError(
            f"Unknown content type: {content_type}"
        )

    # Save only after successful processing.
    remember(content)

    print()
    print("Content saved to history.")
    print()


if __name__ == "__main__":
    main()
