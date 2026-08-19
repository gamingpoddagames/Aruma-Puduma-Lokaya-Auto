import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parent.parent

FONT = BASE_DIR / "assets" / "fonts" / "NotoSansSinhala-Regular.ttf"

IMAGE_DIR = BASE_DIR / "output" / "images"
REEL_DIR = BASE_DIR / "output" / "reels"

WIDTH = 1080
IMAGE_HEIGHT = 1350
REEL_HEIGHT = 1920


def get_font(size):
    if not FONT.exists():
        raise FileNotFoundError(
            f"Sinhala font not found: {FONT}"
        )

    return ImageFont.truetype(
        str(FONT),
        size
    )


def draw_centered_text(
    draw,
    text,
    y,
    font,
    width,
    spacing=12
):
    lines = []
    words = text.split()

    current = ""

    for word in words:

        test = (
            current + " " + word
            if current
            else word
        )

        box = draw.textbbox(
            (0, 0),
            test,
            font=font
        )

        if box[2] <= width - 120:
            current = test
        else:
            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    current_y = y

    for line in lines:

        box = draw.textbbox(
            (0, 0),
            line,
            font=font
        )

        text_width = box[2] - box[0]

        x = (
            WIDTH - text_width
        ) / 2

        draw.text(
            (x + 3, current_y + 3),
            line,
            font=font,
            fill="black"
        )

        draw.text(
            (x, current_y),
            line,
            font=font,
            fill="white"
        )

        current_y += (
            box[3] - box[1]
            + spacing
        )

    return current_y


def create_background(
    width,
    height,
    frame=0
):

    image = Image.new(
        "RGB",
        (width, height),
        (30, 60, 100)
    )

    draw = ImageDraw.Draw(image)

    # Decorative circles.
    for i in range(12):

        x = (
            (i * 197 + frame * 2)
            % width
        )

        y = (
            (i * 131)
            % height
        )

        radius = 40 + (i % 4) * 20

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=(50, 90, 140)
        )

    return image


def create_image(content):

    IMAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    image = create_background(
        WIDTH,
        IMAGE_HEIGHT
    )

    draw = ImageDraw.Draw(image)

    title_font = get_font(70)
    body_font = get_font(48)
    small_font = get_font(38)

    y = 100

    y = draw_centered_text(
        draw,
        f"{content['emoji']} {content['title']}",
        y,
        title_font,
        WIDTH
    )

    y += 60

    y = draw_centered_text(
        draw,
        content["fact"],
        y,
        body_font,
        WIDTH
    )

    y += 80

    draw_centered_text(
        draw,
        "අරුම පුදුම ලෝකය 🌍",
        y,
        small_font,
        WIDTH
    )

    output = (
        IMAGE_DIR
        / f"{content['content_id']}.png"
    )

    image.save(
        output,
        "PNG"
    )

    return output


def create_reel(content):

    REEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    frames_dir = (
        REEL_DIR
        / f"{content['content_id']}_frames"
    )

    frames_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    fps = 30
    duration = 8
    total_frames = fps * duration

    title_font = get_font(76)
    body_font = get_font(52)
    footer_font = get_font(40)

    for frame_number in range(total_frames):

        image = create_background(
            WIDTH,
            REEL_HEIGHT,
            frame_number
        )

        draw = ImageDraw.Draw(image)

        # Animated vertical movement.
        offset = int(
            40 * math.sin(
                frame_number / 25
            )
        )

        y = 300 + offset

        y = draw_centered_text(
            draw,
            f"{content['emoji']} {content['title']}",
            y,
            title_font,
            WIDTH
        )

        y += 70

        draw_centered_text(
            draw,
            content["fact"],
            y,
            body_font,
            WIDTH
        )

        draw_centered_text(
            draw,
            "අරුම පුදුම ලෝකය 🌍",
            1750,
            footer_font,
            WIDTH
        )

        frame_path = (
            frames_dir
            / f"frame_{frame_number:05d}.png"
        )

        image.save(
            frame_path,
            "PNG"
        )

    output = (
        REEL_DIR
        / f"{content['content_id']}.mp4"
    )

    command = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(fps),
        "-i",
        str(frames_dir / "frame_%05d.png"),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(output)
    ]

    subprocess.run(
        command,
        check=True
    )

    return output
