import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

IMAGE_DIR = BASE_DIR / "output" / "images"
REEL_DIR = BASE_DIR / "output" / "reels"


# ============================================================
# VIDEO SETTINGS
# ============================================================

IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1350

REEL_WIDTH = 1080
REEL_HEIGHT = 1920

FPS = 30
REEL_SECONDS = 10


# ============================================================
# FIND SINHALA FONT
# ============================================================

def find_sinhala_font():

    possible_fonts = [

        # Repository fonts
        BASE_DIR / "assets" / "fonts" /
        "NotoSansSinhala-Regular.ttf",

        BASE_DIR / "assets" / "fonts" /
        "NotoSansSinhala[wght].ttf",

        BASE_DIR / "assets" / "fonts" /
        "NotoSansSinhala-VariableFont_wght.ttf",

        # Ubuntu Noto fonts
        Path(
            "/usr/share/fonts/truetype/noto/"
            "NotoSansSinhala-Regular.ttf"
        ),

        Path(
            "/usr/share/fonts/opentype/noto/"
            "NotoSansSinhala-Regular.ttf"
        ),
    ]

    for font in possible_fonts:

        if font.exists():

            print(
                f"Using Sinhala font: {font}"
            )

            return font

    # Search system fonts
    font_directories = [

        Path("/usr/share/fonts"),
        Path("/usr/local/share/fonts")
    ]

    for directory in font_directories:

        if directory.exists():

            for font in directory.rglob(
                "*.ttf"
            ):

                name = font.name.lower()

                if (
                    "sinhala" in name
                    or "noto" in name
                ):

                    print(
                        f"Using system font: {font}"
                    )

                    return font

    raise FileNotFoundError(
        "No Sinhala-compatible font found."
    )


# ============================================================
# FONT
# ============================================================

def get_font(size):

    font_path = find_sinhala_font()

    return ImageFont.truetype(
        str(font_path),
        size
    )


# ============================================================
# TEXT WRAPPING
# ============================================================

def wrap_text(
    draw,
    text,
    font,
    max_width
):

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

        width = (
            box[2] - box[0]
        )

        if width <= max_width:

            current = test

        else:

            if current:

                lines.append(
                    current
                )

            current = word

    if current:

        lines.append(
            current
        )

    return lines


# ============================================================
# CENTER TEXT
# ============================================================

def draw_center_text(
    draw,
    text,
    y,
    font,
    width,
    max_width,
    fill="white",
    stroke=5
):

    lines = wrap_text(
        draw,
        text,
        font,
        max_width
    )

    line_height = (
        font.size + 18
    )

    current_y = y

    for line in lines:

        box = draw.textbbox(
            (0, 0),
            line,
            font=font,
            stroke_width=stroke
        )

        line_width = (
            box[2] - box[0]
        )

        x = (
            width - line_width
        ) // 2

        draw.text(
            (
                x,
                current_y
            ),
            line,
            font=font,
            fill=fill,
            stroke_width=stroke,
            stroke_fill="black"
        )

        current_y += line_height

    return current_y


# ============================================================
# BACKGROUND
# ============================================================

def make_background(
    category,
    width,
    height,
    frame=0
):

    if category == "animals":

        base = (
            10,
            80,
            105
        )

    elif category == "space":

        base = (
            8,
            10,
            45
        )

    elif category == "nature":

        base = (
            20,
            100,
            50
        )

    elif category == "sri_lanka":

        base = (
            95,
            55,
            20
        )

    elif category == "earth":

        base = (
            10,
            70,
            130
        )

    elif category == "technology":

        base = (
            15,
            30,
            65
        )

    else:

        base = (
            30,
            50,
            80
        )

    image = Image.new(
        "RGB",
        (
            width,
            height
        ),
        base
    )

    draw = ImageDraw.Draw(
        image
    )

    # Animated bubbles
    for i in range(20):

        x = (
            i * 173
            + frame * (
                1 + i % 3
            )
        ) % width

        y = (
            i * 113
            + frame // 2
        ) % height

        radius = (
            10 + i % 5 * 5
        )

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            outline=(
                min(255, base[0] + 40),
                min(255, base[1] + 40),
                min(255, base[2] + 40)
            ),
            width=2
        )

    return image


# ============================================================
# OCTOPUS
# ============================================================

def draw_octopus(
    draw,
    cx,
    cy,
    scale=1.0
):

    color = (
        180,
        70,
        160
    )

    dark = (
        120,
        40,
        110
    )

    radius = int(
        150 * scale
    )

    # Head
    draw.ellipse(
        (
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius
        ),
        fill=color,
        outline="white",
        width=6
    )

    # Eyes
    for eye_x in [
        cx - int(55 * scale),
        cx + int(55 * scale)
    ]:

        er = int(
            25 * scale
        )

        draw.ellipse(
            (
                eye_x - er,
                cy - 50,
                eye_x + er,
                cy
            ),
            fill="white"
        )

        pr = int(
            10 * scale
        )

        draw.ellipse(
            (
                eye_x - pr,
                cy - 42,
                eye_x + pr,
                cy - 20
            ),
            fill="black"
        )

    # Smile
    draw.arc(
        (
            cx - 50,
            cy + 20,
            cx + 50,
            cy + 80
        ),
        0,
        180,
        fill="black",
        width=5
    )

    # Tentacles
    for i in range(8):

        x1 = (
            cx
            - int(130 * scale)
            + i * int(
                37 * scale
            )
        )

        y1 = (
            cy
            + int(90 * scale)
        )

        x2 = (
            x1
            + int(
                math.sin(i)
                * 40
                * scale
            )
        )

        y2 = (
            cy
            + int(280 * scale)
        )

        draw.line(
            (
                x1,
                y1,
                x2,
                y2
            ),
            fill=color,
            width=int(
                35 * scale
            )
        )


# ============================================================
# ELEPHANT
# ============================================================

def draw_elephant(
    draw,
    cx,
    cy,
    scale=1.0
):

    grey = (
        125,
        130,
        135
    )

    dark = (
        80,
        85,
        90
    )

    # Body
    draw.ellipse(
        (
            cx - 220,
            cy - 100,
            cx + 220,
            cy + 180
        ),
        fill=grey,
        outline="white",
        width=6
    )

    # Head
    draw.ellipse(
        (
            cx - 160,
            cy - 240,
            cx + 100,
            cy + 20
        ),
        fill=grey,
        outline="white",
        width=6
    )

    # Ear
    draw.ellipse(
        (
            cx - 190,
            cy - 170,
            cx - 40,
            cy - 20
        ),
        fill=(
            105,
            110,
            115
        ),
        outline="white",
        width=4
    )

    # Eye
    draw.ellipse(
        (
            cx - 70,
            cy - 120,
            cx - 40,
            cy - 90
        ),
        fill="black"
    )

    # Trunk
    draw.line(
        (
            cx + 50,
            cy - 30,
            cx + 80,
            cy + 150,
            cx + 20,
            cy + 220
        ),
        fill=grey,
        width=65
    )

    # Legs
    for offset in [
        -140,
        -45,
        70,
        150
    ]:

        draw.rounded_rectangle(
            (
                cx + offset,
                cy + 100,
                cx + offset + 55,
                cy + 300
            ),
            radius=20,
            fill=dark
        )


# ============================================================
# DOLPHIN
# ============================================================

def draw_dolphin(
    draw,
    cx,
    cy,
    scale=1.0
):

    blue = (
        60,
        160,
        210
    )

    dark = (
        35,
        100,
        150
    )

    # Body
    draw.ellipse(
        (
            cx - 250,
            cy - 90,
            cx + 250,
            cy + 90
        ),
        fill=blue,
        outline="white",
        width=6
    )

    # Nose
    draw.polygon(
        [
            (
                cx + 220,
                cy - 20
            ),
            (
                cx + 360,
                cy
            ),
            (
                cx + 220,
                cy + 30
            )
        ],
        fill=blue,
        outline="white"
    )

    # Dorsal fin
    draw.polygon(
        [
            (
                cx,
                cy - 70
            ),
            (
                cx + 40,
                cy - 180
            ),
            (
                cx + 100,
                cy - 60
            )
        ],
        fill=dark
    )

    # Tail
    draw.polygon(
        [
            (
                cx - 230,
                cy
            ),
            (
                cx - 360,
                cy - 90
            ),
            (
                cx - 310,
                cy
            ),
            (
                cx - 360,
                cy + 90
            )
        ],
        fill=blue,
        outline="white"
    )

    # Eye
    draw.ellipse(
        (
            cx + 130,
            cy - 50,
            cx + 160,
            cy - 20
        ),
        fill="black"
    )


# ============================================================
# SUN
# ============================================================

def draw_sun(
    draw,
    cx,
    cy
):

    yellow = (
        255,
        190,
        30
    )

    radius = 140

    draw.ellipse(
        (
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius
        ),
        fill=yellow,
        outline="white",
        width=6
    )

    for angle in range(
        0,
        360,
        30
    ):

        rad = math.radians(
            angle
        )

        x1 = (
            cx
            + int(
                math.cos(rad)
                * 180
            )
        )

        y1 = (
            cy
            + int(
                math.sin(rad)
                * 180
            )
        )

        x2 = (
            cx
            + int(
                math.cos(rad)
                * 250
            )
        )

        y2 = (
            cy
            + int(
                math.sin(rad)
                * 250
            )
        )

        draw.line(
            (
                x1,
                y1,
                x2,
                y2
            ),
            fill=yellow,
            width=12
        )


# ============================================================
# MOON
# ============================================================

def draw_moon(
    draw,
    cx,
    cy
):

    radius = 180

    draw.ellipse(
        (
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius
        ),
        fill=(
            225,
            225,
            205
        ),
        outline="white",
        width=5
    )

    # shadow creates crescent-like appearance
    draw.ellipse(
        (
            cx - radius + 65,
            cy - radius,
            cx + radius + 65,
            cy + radius
        ),
        fill=(
            8,
            10,
            45
        )
    )

    # craters
    for x, y, r in [
        (-70, -50, 20),
        (-40, 60, 28),
        (-90, 100, 15)
    ]:

        draw.ellipse(
            (
                cx + x - r,
                cy + y - r,
                cx + x + r,
                cy + y + r
            ),
            fill=(
                180,
                180,
                165
            )
        )


# ============================================================
# BAMBOO
# ============================================================

def draw_bamboo(
    draw,
    cx,
    cy
):

    green = (
        50,
        160,
        70
    )

    dark = (
        25,
        100,
        45
    )

    for offset in [
        -80,
        0,
        80
    ]:

        x = cx + offset

        draw.line(
            (
                x,
                cy + 250,
                x + 30,
                cy - 300
            ),
            fill=green,
            width=35
        )

        for y in range(
            cy - 250,
            cy + 250,
            100
        ):

            draw.line(
                (
                    x - 20,
                    y,
                    x + 50,
                    y
                ),
                fill=dark,
                width=8
            )

        # leaves
        draw.ellipse(
            (
                x - 120,
                cy - 200,
                x - 20,
                cy - 120
            ),
            fill=green
        )

        draw.ellipse(
            (
                x + 20,
                cy - 120,
                x + 130,
                cy - 40
            ),
            fill=green
        )


# ============================================================
# SIGIRIYA
# ============================================================

def draw_sigiriya(
    draw,
    width,
    height
):

    ground = int(
        height * 0.78
    )

    # ground
    draw.rectangle(
        (
            0,
            ground,
            width,
            height
        ),
        fill=(
            30,
            100,
            45
        )
    )

    # rock
    draw.polygon(
        [
            (
                width // 2 - 300,
                ground
            ),
            (
                width // 2 - 180,
                ground - 430
            ),
            (
                width // 2 - 70,
                ground - 520
            ),
            (
                width // 2 + 80,
                ground - 470
            ),
            (
                width // 2 + 250,
                ground
            )
        ],
        fill=(
            125,
            70,
            40
        ),
        outline="white"
    )

    # top palace
    draw.rectangle(
        (
            width // 2 - 90,
            ground - 520,
            width // 2 + 90,
            ground - 450
        ),
        fill=(
            190,
            150,
            70
        ),
        outline="white",
        width=4
    )


# ============================================================
# CRICKET
# ============================================================

def draw_cricket(
    draw,
    cx,
    cy
):

    red = (
        170,
        30,
        30
    )

    brown = (
        190,
        150,
        80
    )

    # Ball
    r = 110

    draw.ellipse(
        (
            cx - r,
            cy - r,
            cx + r,
            cy + r
        ),
        fill=red,
        outline="white",
        width=6
    )

    draw.arc(
        (
            cx - r + 20,
            cy - r + 20,
            cx + r - 20,
            cy + r - 20
        ),
        60,
        300,
        fill="white",
        width=6
    )

    # Bat
    draw.rounded_rectangle(
        (
            cx + 140,
            cy - 300,
            cx + 230,
            cy + 250
        ),
        radius=25,
        fill=brown,
        outline="white",
        width=5
    )

    draw.line(
        (
            cx + 185,
            cy + 250,
            cx + 185,
            cy + 400
        ),
        fill=brown,
        width=50
    )


# ============================================================
# OCEAN
# ============================================================

def draw_ocean(
    draw,
    width,
    height,
    frame=0
):

    water_top = 550

    draw.rectangle(
        (
            0,
            water_top,
            width,
            height
        ),
        fill=(
            15,
            120,
            190
        )
    )

    # waves
    for y in range(
        water_top + 40,
        height,
        100
    ):

        for x in range(
            -100,
            width + 100,
            200
        ):

            offset = int(
                math.sin(
                    (
                        frame
                        + x
                    ) / 30
                ) * 20
            )

            draw.arc(
                (
                    x,
                    y + offset,
                    x + 180,
                    y + 80 + offset
                ),
                180,
                360,
                fill="white",
                width=5
            )

    # sun
    draw.ellipse(
        (
            800,
            180,
            970,
            350
        ),
        fill=(
            255,
            200,
            50
        )
    )


# ============================================================
# INTERNET
# ============================================================

def draw_internet(
    draw,
    cx,
    cy
):

    blue = (
        40,
        150,
        230
    )

    radius = 220

    draw.ellipse(
        (
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius
        ),
        fill=blue,
        outline="white",
        width=7
    )

    # longitude
    draw.ellipse(
        (
            cx - 90,
            cy - radius,
            cx + 90,
            cy + radius
        ),
        outline="white",
        width=6
    )

    # latitude
    draw.arc(
        (
            cx - radius,
            cy - 100,
            cx + radius,
            cy + 100
        ),
        0,
        360,
        fill="white",
        width=6
    )

    # horizontal line
    draw.line(
        (
            cx - radius,
            cy,
            cx + radius,
            cy
        ),
        fill="white",
        width=6
    )


# ============================================================
# DRAW EXACT VISUAL
# ============================================================

def draw_visual(
    draw,
    visual,
    width,
    height,
    frame=0
):

    cx = width // 2

    # Place main object around upper-middle area
    cy = int(
        height * 0.40
    )

    if visual == "octopus":

        draw_octopus(
            draw,
            cx,
            cy
        )

    elif visual == "elephant":

        draw_elephant(
            draw,
            cx,
            cy
        )

    elif visual == "dolphin":

        draw_dolphin(
            draw,
            cx,
            cy
        )

    elif visual == "sun":

        draw_sun(
            draw,
            cx,
            cy
        )

    elif visual == "moon":

        draw_moon(
            draw,
            cx,
            cy
        )

    elif visual == "bamboo":

        draw_bamboo(
            draw,
            cx,
            cy
        )

    elif visual == "sigiriya":

        draw_sigiriya(
            draw,
            width,
            height
        )

    elif visual == "cricket":

        draw_cricket(
            draw,
            cx,
            cy
        )

    elif visual == "ocean":

        draw_ocean(
            draw,
            width,
            height,
            frame
        )

    elif visual == "internet":

        draw_internet(
            draw,
            cx,
            cy
        )

    else:

        # Generic fallback
        draw.ellipse(
            (
                cx - 150,
                cy - 150,
                cx + 150,
                cy + 150
            ),
            fill=(
                80,
                140,
                200
            ),
            outline="white",
            width=6
        )


# ============================================================
# CREATE IMAGE
# ============================================================

def create_image(content):

    IMAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    image = make_background(
        content.get(
            "category",
            "general"
        ),
        IMAGE_WIDTH,
        IMAGE_HEIGHT
    )

    draw = ImageDraw.Draw(
        image
    )

    # Fonts
    title_font = get_font(70)
    fact_font = get_font(48)
    footer_font = get_font(38)

    # Exact visual
    draw_visual(
        draw,
        content.get(
            "visual",
            content.get(
                "category",
                "general"
            )
        ),
        IMAGE_WIDTH,
        IMAGE_HEIGHT
    )

    # Title
    draw_center_text(
        draw,
        content["title"],
        780,
        title_font,
        IMAGE_WIDTH,
        IMAGE_WIDTH - 100
    )

    # Fact
    draw_center_text(
        draw,
        content["fact"],
        950,
        fact_font,
        IMAGE_WIDTH,
        IMAGE_WIDTH - 120
    )

    # Branding
    draw_center_text(
        draw,
        "අරුම පුදුම ලෝකය 🌍",
        1250,
        footer_font,
        IMAGE_WIDTH,
        IMAGE_WIDTH - 100
    )

    output = (
        IMAGE_DIR
        / f"{content['content_id']}.png"
    )

    image.save(
        output,
        "PNG"
    )

    print(
        f"Image created: {output}"
    )

    return output


# ============================================================
# CREATE REEL
# ============================================================

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
        FPS
        * REEL_SECONDS
    )

    title_font = get_font(76)
    fact_font = get_font(54)
    footer_font = get_font(40)

    print(
        f"Creating {total_frames} Reel frames..."
    )

    for frame_number in range(
        total_frames
    ):

        image = make_background(
            content.get(
                "category",
                "general"
            ),
            REEL_WIDTH,
            REEL_HEIGHT,
            frame_number
        )

        draw = ImageDraw.Draw(
            image
        )

        # Exact content visual
        draw_visual(
            draw,
            content.get(
                "visual",
                content.get(
                    "category",
                    "general"
                )
            ),
            REEL_WIDTH,
            REEL_HEIGHT,
            frame_number
        )

        # Animated title
        movement = int(
            25 * math.sin(
                frame_number / 15
            )
        )

        draw_center_text(
            draw,
            content["title"],
            160 + movement,
            title_font,
            REEL_WIDTH,
            REEL_WIDTH - 100
        )

        # Fact
        draw_center_text(
            draw,
            content["fact"],
            1050,
            fact_font,
            REEL_WIDTH,
            REEL_WIDTH - 120
        )

        # CTA
        draw_center_text(
            draw,
            "ඔබේ අදහස Comment කරන්න! 💬",
            1550,
            footer_font,
            REEL_WIDTH,
            REEL_WIDTH - 100
        )

        # Page name
        draw_center_text(
            draw,
            "අරුම පුදුම ලෝකය 🌍",
            1800,
            footer_font,
            REEL_WIDTH,
            REEL_WIDTH - 100
        )

        frame_path = (
            frames_dir
            / f"frame_{frame_number:05d}.png"
        )

        image.save(
            frame_path,
            "PNG"
        )

    # ========================================================
    # FFMPEG
    # ========================================================

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

    print(
        "Rendering Reel with FFmpeg..."
    )

    subprocess.run(
        command,
        check=True
    )

    print(
        f"Reel created: {output}"
    )

    return output
