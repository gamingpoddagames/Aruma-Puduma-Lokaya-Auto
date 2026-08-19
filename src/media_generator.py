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

FPS = 30
REEL_SECONDS = 10


# ---------------------------------------------------------
# FONT
# ---------------------------------------------------------

def get_font(size):

    if not FONT.exists():
        raise FileNotFoundError(
            f"Sinhala font not found:\n{FONT}"
        )

    return ImageFont.truetype(
        str(FONT),
        size
    )


# ---------------------------------------------------------
# TEXT WRAPPING
# ---------------------------------------------------------

def wrap_text(draw, text, font, max_width):

    words = text.split()

    lines = []
    current = ""

    for word in words:

        test = (
            word
            if not current
            else current + " " + word
        )

        box = draw.textbbox(
            (0, 0),
            test,
            font=font
        )

        if box[2] - box[0] <= max_width:

            current = test

        else:

            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


def draw_center_text(
    draw,
    text,
    y,
    font,
    max_width,
    fill="white",
    stroke=4
):

    lines = wrap_text(
        draw,
        text,
        font,
        max_width
    )

    line_height = font.size + 15

    current_y = y

    for line in lines:

        box = draw.textbbox(
            (0, 0),
            line,
            font=font,
            stroke_width=stroke
        )

        width = box[2] - box[0]

        x = (WIDTH - width) // 2

        draw.text(
            (x, current_y),
            line,
            font=font,
            fill=fill,
            stroke_width=stroke,
            stroke_fill="black"
        )

        current_y += line_height

    return current_y


# ---------------------------------------------------------
# BACKGROUND
# ---------------------------------------------------------

def background(category, width, height, frame=0):

    if category == "animals":

        bg = (12, 80, 105)

    elif category == "space":

        bg = (8, 10, 45)

    elif category == "sri_lanka":

        bg = (90, 55, 20)

    elif category == "sports":

        bg = (15, 80, 35)

    elif category == "science":

        bg = (35, 25, 80)

    elif category == "nature":

        bg = (25, 100, 55)

    elif category == "technology":

        bg = (20, 35, 65)

    else:

        bg = (35, 55, 80)

    image = Image.new(
        "RGB",
        (width, height),
        bg
    )

    draw = ImageDraw.Draw(image)

    # Animated decorative circles
    for i in range(15):

        x = (
            i * 173
            + frame * (1 + i % 3)
        ) % width

        y = (
            i * 127
            + frame // 2
        ) % height

        radius = 20 + (i % 4) * 10

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=tuple(
                min(255, c + 30)
                for c in bg
            )
        )

    return image


# ---------------------------------------------------------
# ANIMAL GRAPHIC
# ---------------------------------------------------------

def draw_octopus(draw, cx, cy, scale=1.0):

    # head
    r = int(150 * scale)

    draw.ellipse(
        (
            cx - r,
            cy - r,
            cx + r,
            cy + r
        ),
        fill=(170, 70, 150),
        outline="white",
        width=5
    )

    # eyes
    eye_r = int(22 * scale)

    for ex in (
        cx - int(55 * scale),
        cx + int(55 * scale)
    ):

        draw.ellipse(
            (
                ex - eye_r,
                cy - int(40 * scale),
                ex + eye_r,
                cy + int(5 * scale)
            ),
            fill="white"
        )

        draw.ellipse(
            (
                ex - int(8 * scale),
                cy - int(35 * scale),
                ex + int(8 * scale),
                cy - int(5 * scale)
            ),
            fill="black"
        )

    # tentacles
    for i in range(8):

        x1 = (
            cx
            - int(120 * scale)
            + i * int(35 * scale)
        )

        y1 = cy + int(100 * scale)

        x2 = (
            x1
            + int(
                math.sin(i) * 45 * scale
            )
        )

        y2 = (
            cy
            + int(260 * scale)
        )

        draw.line(
            (x1, y1, x2, y2),
            fill=(170, 70, 150),
            width=int(35 * scale)
        )


# ---------------------------------------------------------
# SPACE GRAPHIC
# ---------------------------------------------------------

def draw_space(draw, width, height, frame=0):

    # stars
    for i in range(50):

        x = (i * 97) % width
        y = (i * 137) % height

        r = 2 + (i % 3)

        draw.ellipse(
            (
                x-r,
                y-r,
                x+r,
                y+r
            ),
            fill="white"
        )

    # moon movement
    moon_x = (
        width // 2
        + int(
            math.sin(frame / 30)
            * 80
        )
    )

    moon_y = 500

    r = 190

    draw.ellipse(
        (
            moon_x-r,
            moon_y-r,
            moon_x+r,
            moon_y+r
        ),
        fill=(220, 220, 200),
        outline="white",
        width=5
    )

    # moon craters
    for i in range(8):

        cx = moon_x - 100 + (i * 47) % 180
        cy = moon_y - 90 + (i * 61) % 170

        rr = 15 + i * 3

        draw.ellipse(
            (
                cx-rr,
                cy-rr,
                cx+rr,
                cy+rr
            ),
            fill=(180, 180, 165)
        )


# ---------------------------------------------------------
# SRI LANKA GRAPHIC
# ---------------------------------------------------------

def draw_sri_lanka(draw, width, height):

    # flag-like panel
    x1 = width // 2 - 280
    y1 = 260
    x2 = width // 2 + 280
    y2 = 600

    draw.rectangle(
        (x1, y1, x2, y2),
        fill=(125, 35, 25),
        outline="white",
        width=6
    )

    # decorative yellow frame
    draw.rectangle(
        (
            x1 + 20,
            y1 + 20,
            x2 - 20,
            y2 - 20
        ),
        outline=(240, 190, 60),
        width=12
    )

    # cricket ball
    cx = width // 2
    cy = 820

    r = 100

    draw.ellipse(
        (
            cx-r,
            cy-r,
            cx+r,
            cy+r
        ),
        fill=(160, 30, 30),
        outline="white",
        width=5
    )

    draw.arc(
        (
            cx-r+15,
            cy-r+15,
            cx+r-15,
            cy+r-15
        ),
        60,
        300,
        fill="white",
        width=5
    )


# ---------------------------------------------------------
# SPORTS GRAPHIC
# ---------------------------------------------------------

def draw_sports(draw, width, height):

    cx = width // 2
    cy = 600

    # cricket ball
    r = 110

    draw.ellipse(
        (
            cx-r,
            cy-r,
            cx+r,
            cy+r
        ),
        fill=(160, 25, 25),
        outline="white",
        width=6
    )

    draw.arc(
        (
            cx-r+20,
            cy-r+20,
            cx+r-20,
            cy+r-20
        ),
        60,
        300,
        fill="white",
        width=6
    )

    # bat
    draw.rounded_rectangle(
        (
            cx + 120,
            cy - 250,
            cx + 210,
            cy + 220
        ),
        radius=30,
        fill=(190, 150, 80),
        outline="white",
        width=5
    )


# ---------------------------------------------------------
# SCIENCE GRAPHIC
# ---------------------------------------------------------

def draw_science(draw, width, height):

    cx = width // 2
    cy = 600

    # atom
    for angle in (0, 60, 120):

        box = (
            cx - 260,
            cy - 110,
            cx + 260,
            cy + 110
        )

        draw.ellipse(
            box,
            outline="white",
            width=8
        )

    draw.ellipse(
        (
            cx - 45,
            cy - 45,
            cx + 45,
            cy + 45
        ),
        fill=(120, 200, 255),
        outline="white",
        width=5
    )


# ---------------------------------------------------------
# NATURE GRAPHIC
# ---------------------------------------------------------

def draw_nature(draw, width, height):

    ground = int(height * 0.72)

    draw.rectangle(
        (
            0,
            ground,
            width,
            height
        ),
        fill=(25, 90, 40)
    )

    # tree
    trunk_x = width // 2

    draw.rectangle(
        (
            trunk_x - 35,
            ground - 300,
            trunk_x + 35,
            ground
        ),
        fill=(110, 65, 35)
    )

    for x, y, r in [
        (trunk_x - 100, ground - 320, 100),
        (trunk_x + 100, ground - 330, 110),
        (trunk_x, ground - 420, 130)
    ]:

        draw.ellipse(
            (
                x-r,
                y-r,
                x+r,
                y+r
            ),
            fill=(35, 150, 65)
        )


# ---------------------------------------------------------
# TECHNOLOGY GRAPHIC
# ---------------------------------------------------------

def draw_technology(draw, width, height):

    cx = width // 2
    cy = 600

    draw.rounded_rectangle(
        (
            cx - 280,
            cy - 180,
            cx + 280,
            cy + 180
        ),
        radius=30,
        fill=(15, 20, 35),
        outline="white",
        width=8
    )

    draw.rectangle(
        (
            cx - 220,
            cy - 120,
            cx + 220,
            cy + 100
        ),
        fill=(30, 100, 160)
    )

    draw.rectangle(
        (
            cx - 120,
            cy + 180,
            cx + 120,
            cy + 215
        ),
        fill="white"
    )


# ---------------------------------------------------------
# CATEGORY GRAPHIC
# ---------------------------------------------------------

def draw_category_graphic(
    draw,
    category,
    width,
    height,
    frame=0
):

    if category == "animals":

        draw_octopus(
            draw,
            width // 2,
            600,
            1.0
        )

    elif category == "space":

        draw_space(
            draw,
            width,
            height,
            frame
        )

    elif category == "sri_lanka":

        draw_sri_lanka(
            draw,
            width,
            height
        )

    elif category == "sports":

        draw_sports(
            draw,
            width,
            height
        )

    elif category == "science":

        draw_science(
            draw,
            width,
            height
        )

    elif category == "nature":

        draw_nature(
            draw,
            width,
            height
        )

    elif category == "technology":

        draw_technology(
            draw,
            width,
            height
        )

    else:

        draw.ellipse(
            (
                width // 2 - 150,
                400,
                width // 2 + 150,
                700
            ),
            fill=(80, 130, 190),
            outline="white",
            width=5
        )


# ---------------------------------------------------------
# IMAGE
# ---------------------------------------------------------

def create_image(content):

    IMAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    image = background(
        content["category"],
        WIDTH,
        IMAGE_HEIGHT
    )

    draw = ImageDraw.Draw(image)

    title_font = get_font(70)
    fact_font = get_font(48)
    footer_font = get_font(38)

    draw_category_graphic(
        draw,
        content["category"],
        WIDTH,
        IMAGE_HEIGHT
    )

    y = 850

    y = draw_center_text(
        draw,
        content["title"],
        y,
        title_font,
        WIDTH - 100
    )

    y += 30

    draw_center_text(
        draw,
        content["fact"],
        y,
        fact_font,
        WIDTH - 120
    )

    draw_center_text(
        draw,
        "අරුම පුදුම ලෝකය 🌍",
        1240,
        footer_font,
        WIDTH - 100
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


# ---------------------------------------------------------
# REEL
# ---------------------------------------------------------

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

    total_frames = (
        FPS * REEL_SECONDS
    )

    title_font = get_font(76)
    fact_font = get_font(54)
    footer_font = get_font(40)

    for frame_number in range(
        total_frames
    ):

        image = background(
            content["category"],
            WIDTH,
            REEL_HEIGHT,
            frame_number
        )

        draw = ImageDraw.Draw(image)

        # Content-aware illustration
        draw_category_graphic(
            draw,
            content["category"],
            WIDTH,
            REEL_HEIGHT,
            frame_number
        )

        # Animated title
        title_offset = int(
            50 * math.sin(
                frame_number / 18
            )
        )

        draw_center_text(
            draw,
            content["title"],
            170 + title_offset,
            title_font,
            WIDTH - 100
        )

        # Fact
        draw_center_text(
            draw,
            content["fact"],
            1050,
            fact_font,
            WIDTH - 120
        )

        # Footer
        draw_center_text(
            draw,
            "අරුම පුදුම ලෝකය 🌍",
            1780,
            footer_font,
            WIDTH - 100
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
        str(FPS),
        "-i",
        str(
            frames_dir
            / "frame_%05d.png"
        ),
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "23",
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
