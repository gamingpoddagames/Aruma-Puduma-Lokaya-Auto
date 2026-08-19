from src.local_content_engine import make_content
from src.media_generator import create_image, create_reel


def main():
    content = make_content()

    print("\nSelected content:")
    print(content["text"])

    print("\nCreating image...")
    image = create_image(content)
    print(f"Image created: {image}")

    print("\nCreating Reel...")
    reel = create_reel(content)
    print(f"Reel created: {reel}")

    print("\nDONE!")


if __name__ == "__main__":
    main()
