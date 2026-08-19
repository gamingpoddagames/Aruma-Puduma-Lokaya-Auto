from src.content_engine import choose_content, remember_content
from src.facebook import publish_text_post


def main():
    content = choose_content()

    print("Selected content:")
    print(content["text"])

    result = publish_text_post(content["text"])

    print("Facebook response:")
    print(result)

    remember_content(content)

    print("Content saved to history.")


if __name__ == "__main__":
    main()
