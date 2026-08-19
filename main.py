from src.local_content_engine import (
    make_content,
    remember
)

from src.media_generator import (
    create_image,
    create_reel
)

from src.facebook import (
    publish_text_post,
    publish_image_post,
    publish_reel
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

    # --------------------------------
    # TEXT
    # --------------------------------

    if content_type == "text":

        print("Publishing Facebook text post...")

        result = publish_text_post(
            content["text"]
        )

        print("Facebook response:")
        print(result)

    # --------------------------------
    # IMAGE
    # --------------------------------

    elif content_type == "image":

        print("Creating image...")

        image_path = create_image(
            content
        )

        print(
            "Image created:",
            image_path
        )

        print("Publishing image...")

        result = publish_image_post(
            image_path,
            content["text"]
        )

        print("Facebook response:")
        print(result)

    # --------------------------------
    # REEL
    # --------------------------------

    elif content_type == "reel":

        print("Creating Reel...")

        reel_path = create_reel(
            content
        )

        print(
            "Reel created:",
            reel_path
        )

        print("Publishing Reel...")

        result = publish_reel(
            reel_path,
            content["text"]
        )

        print("Facebook response:")
        print(result)

    else:

        raise RuntimeError(
            f"Unknown content type: {content_type}"
        )

    # Only remember after successful publishing.
    remember(content)

    print()
    print("Content successfully published.")
    print("Content saved to history.")
    print()


if __name__ == "__main__":
    main()
