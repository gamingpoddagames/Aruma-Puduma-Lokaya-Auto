from pathlib import Path
import math
import subprocess

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "output"

IMAGE_DIR = OUTPUT_DIR / "images"
REEL_DIR = OUTPUT_DIR / "reels"


# ============================================================
# SETTINGS
# ============================================================

IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1350

REEL_WIDTH = 1080
REEL_HEIGHT = 1920

FPS = 30
REEL_SECONDS = 10


# ============================================================
# FONT
# ============================================================

def find_font():

    candidates = [

        # Project font
        BASE_DIR / "assets" / "fonts" / "NotoSansSinhala-Regular.ttf",

        BASE_DIR / "assets" / "fonts" / "NotoSansSinhala[wght].ttf",

        BASE_DIR / "assets" / "fonts" / "NotoSansSinhala-VariableFont_wght.ttf",

        # Ubuntu
        Path(
            "/usr/share/fonts/truetype/noto/"
            "NotoSansSinhala-Regular.ttf"
        ),

        Path(
            "/usr/share/fonts/opentype/noto/"
            "NotoSansSinhala-Regular.ttf"
        ),
    ]

    for path in candidates:

        if path.exists():

            print(
                f"[FONT] Using: {path}"
            )

            return path

    # Search all system fonts
    search_dirs = [
        Path("/usr/share/fonts"),
        Path("/usr/local/share/fonts"),
        Path.home() / ".fonts",
    ]

    for directory in search_dirs:

        if not directory.exists():
            continue

        for path in directory.rglob("*.ttf"):

            name = path.name.lower()

            if "sinhala" in name:

                print(
                    f"[FONT] Found Sinhala font: {path}"
                )

                return path

    # Last fallback
    for directory in search_dirs:

        if not directory.exists():
            continue

        for path in directory.rglob("*.ttf"):

            if "noto" in path.name.lower():

                print(
                    f"[FONT] Using Noto fallback: {path}"
                )

                return path

    raise FileNotFoundError(
        "\n"
        "==================================================\n"
        "SINHALA FONT NOT FOUND\n"
        "==================================================\n"
        "Install Noto Sans Sinhala or place it in:\n"
        f"{BASE_DIR / 'assets' / 'fonts'}\n"
        "=================================================="
    )


def get_font(size):

    font = find_font()

    return ImageFont.truetype(
        str(font),
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

    if not words:
        return []

    lines = []

    current = ""

    for word in words:

        candidate = (
            word
            if not current
            else current + " " + word
        )

        box = draw.textbbox(
            (0, 0),
            candidate,
            font=font
        )

        width = box[2] - box[0]

        if width <= max_width:

            current = candidate

        else:

            if current:

                lines.append(current)

            current = word

    if current:

        lines.append(current)

    return lines


# ============================================================
# CENTER TEXT
# ============================================================

def draw_center_text(
    draw,
    text,
    y,
    font,
    canvas_width,
    max_width,
    fill="white",
    stroke_width=4
):

    lines = wrap_text(
        draw,
        text,
        font,
        max_width
    )

    line_height = font.size + 18

    current_y = y

    for line in lines:

        box = draw.textbbox(
            (0, 0),
            line,
            font=font,
            stroke_width=stroke_width
        )

        width = box[2] - box[0]

        x = (
            canvas_width - width
        ) // 2

        draw.text(
            (
                x,
                current_y
            ),
            line,
            font=font,
            fill=fill,
            stroke_width=stroke_width,
            stroke_fill="black"
        )

        current_y += line_height

    return current_y


# ============================================================
# BACKGROUND
# ============================================================

def create_background(
    category,
    width,
    height,
    frame=0
):

    backgrounds = {

        "animals":
            (20, 100, 120),

        "space":
            (8, 12, 55),

        "nature":
            (25, 110, 55),

        "sri_lanka":
            (100, 60, 25),

        "earth":
            (10, 80, 140),

        "technology":
            (15, 35, 75),

        "general":
            (35, 55, 90),
    }

    bg = backgrounds.get(
        category,
        backgrounds["general"]
    )

    image = Image.new(
        "RGB",
        (
            width,
            height
        ),
        bg
    )

    draw = ImageDraw.Draw(image)

    # Animated particles
    for i in range(25):

        x = (
            i * 191
            + frame * (1 + i % 3)
        ) % width

        y = (
            i * 137
            + frame // 2
        ) % height

        r = 5 + (i % 5) * 3

        draw.ellipse(
            (
                x - r,
                y - r,
                x + r,
                y + r
            ),
            outline="white",
            width=2
        )

    return image


# ============================================================
# OCTOPUS
# ============================================================

def draw_octopus(
    draw,
    cx,
    cy
):

    purple = (
        180,
        65,
        165
    )

    dark = (
        115,
        35,
        105
    )

    # Head
    draw.ellipse(
        (
            cx - 170,
            cy - 170,
            cx + 170,
            cy + 170
        ),
        fill=purple,
        outline="white",
        width=7
    )

    # Eyes
    for x in (
        cx - 60,
        cx + 60
    ):

        draw.ellipse(
            (
                x - 28,
                cy - 60,
                x + 28,
                cy
            ),
            fill="white"
        )

        draw.ellipse(
            (
                x - 11,
                cy - 45,
                x + 11,
                cy - 22
            ),
            fill="black"
        )

    # Mouth
    draw.arc(
        (
            cx - 55,
            cy + 10,
            cx + 55,
            cy + 80
        ),
        0,
        180,
        fill="black",
        width=7
    )

    # Tentacles
    for i in range(8):

        x = (
            cx - 140
            + i * 40
        )

        draw.line(
            (
                x,
                cy + 110,
                x - 30 + i * 8,
                cy + 330
            ),
            fill=purple,
            width=45
        )


# ============================================================
# ELEPHANT
# ============================================================

def draw_elephant(
    draw,
    cx,
    cy
):

    grey = (
        135,
        140,
        145
    )

    dark = (
        90,
        95,
        100
    )

    # Body
    draw.ellipse(
        (
            cx - 260,
            cy - 80,
            cx + 240,
            cy + 220
        ),
        fill=grey,
        outline="white",
        width=7
    )

    # Head
    draw.ellipse(
        (
            cx - 180,
            cy - 260,
            cx + 100,
            cy + 40
        ),
        fill=grey,
        outline="white",
        width=7
    )

    # Ear
    draw.ellipse(
        (
            cx - 230,
            cy - 200,
            cx - 50,
            cy + 10
        ),
        fill=dark,
        outline="white",
        width=5
    )

    # Eye
    draw.ellipse(
        (
            cx - 65,
            cy - 130,
            cx - 30,
            cy - 95
        ),
        fill="black"
    )

    # Trunk
    draw.line(
        (
            cx + 40,
            cy - 20,
            cx + 80,
            cy + 160,
            cx + 20,
            cy + 240
        ),
        fill=grey,
        width=70
    )

    # Legs
    for offset in (
        -150,
        -40,
        80,
        160
    ):

        draw.rounded_rectangle(
            (
                cx + offset,
                cy + 100,
                cx + offset + 60,
                cy + 330
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
    cy
):

    blue = (
        60,
        170,
        220
    )

    dark = (
        30,
        105,
        160
    )

    # Body
    draw.ellipse(
        (
            cx - 270,
            cy - 90,
            cx + 250,
            cy + 90
        ),
        fill=blue,
        outline="white",
        width=7
    )

    # Nose
    draw.polygon(
        [
            (
                cx + 210,
                cy - 40
            ),
            (
                cx + 390,
                cy
            ),
            (
                cx + 210,
                cy + 40
            )
        ],
        fill=blue,
        outline="white"
    )

    # Tail
    draw.polygon(
        [
            (
                cx - 230,
                cy
            ),
            (
                cx - 390,
                cy - 110
            ),
            (
                cx - 320,
                cy
            ),
            (
                cx - 390,
                cy + 110
            )
        ],
        fill=blue,
        outline="white"
    )

    # Fin
    draw.polygon(
        [
            (
                cx,
                cy - 70
            ),
            (
                cx + 50,
                cy - 190
            ),
            (
                cx + 100,
                cy - 50
            )
        ],
        fill=dark
    )

    # Eye
    draw.ellipse(
        (
            cx + 120,
            cy - 45,
            cx + 150,
            cy - 15
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
        200,
        40
    )

    radius = 150

    draw.ellipse(
        (
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius
        ),
        fill=yellow,
        outline="white",
        width=7
    )

    for angle in range(
        0,
        360,
        30
    ):

        rad = math.radians(angle)

        x1 = cx + int(
            math.cos(rad) * 190
        )

        y1 = cy + int(
            math.sin(rad) * 190
        )

        x2 = cx + int(
            math.cos(rad) * 260
        )

        y2 = cy + int(
            math.sin(rad) * 260
        )

        draw.line(
            (
                x1,
                y1,
                x2,
                y2
            ),
            fill=yellow,
            width=14
        )


# ============================================================
# MOON
# ============================================================

def draw_moon(
    draw,
    cx,
    cy
):

    moon_color = (
        235,
        235,
        210
    )

    dark = (
        8,
        12,
        55
    )

    r = 190

    draw.ellipse(
        (
            cx - r,
            cy - r,
            cx + r,
            cy + r
        ),
        fill=moon_color,
        outline="white",
        width=6
    )

    # Crescent
    draw.ellipse(
        (
            cx - r + 85,
            cy - r - 5,
            cx + r + 85,
            cy + r - 5
        ),
        fill=dark
    )

    # Craters
    for dx, dy, rr in (
        (-80, -50, 22),
        (-60, 80, 28),
        (-105, 100, 14)
    ):

        draw.ellipse(
            (
                cx + dx - rr,
                cy + dy - rr,
                cx + dx + rr,
                cy + dy + rr
            ),
            fill=(
                185,
                185,
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
        170,
        70
    )

    dark = (
        25,
        105,
        40
    )

    for offset in (
        -100,
        0,
        100
    ):

        x = cx + offset

        draw.line(
            (
                x,
                cy + 350,
                x + 30,
                cy - 350
            ),
            fill=green,
            width=45
        )

        for y in range(
            cy - 300,
            cy + 300,
            100
        ):

            draw.line(
                (
                    x - 25,
                    y,
                    x + 55,
                    y
                ),
                fill=dark,
                width=8
            )

        # Leaves
        draw.ellipse(
            (
                x - 150,
                cy - 200,
                x - 20,
                cy - 100
            ),
            fill=green
        )

        draw.ellipse(
            (
                x + 20,
                cy - 80,
                x + 150,
                cy + 20
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

    ground = 1350

    # Ground
    draw.rectangle(
        (
            0,
            ground,
            width,
            height
        ),
        fill=(
            30,
            105,
            45
        )
    )

    cx = width // 2

    # Rock
    draw.polygon(
        [
            (
                cx - 360,
                ground
            ),
            (
                cx - 260,
                ground - 500
            ),
            (
                cx - 100,
                ground - 650
            ),
            (
                cx + 100,
                ground - 620
            ),
            (
                cx + 300,
                ground - 300
            ),
            (
                cx + 380,
                ground
            )
        ],
        fill=(
            130,
            75,
            40
        ),
        outline="white"
    )

    # Palace
    draw.rectangle(
        (
            cx - 120,
            ground - 650,
            cx + 120,
            ground - 570
        ),
        fill=(
            190,
            150,
            70
        ),
        outline="white",
        width=5
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
        180,
        30,
        30
    )

    brown = (
        190,
        145,
        75
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
        width=7
    )

    draw.arc(
        (
            cx - 80,
            cy - 80,
            cx + 80,
            cy + 80
        ),
        60,
        300,
        fill="white",
        width=6
    )

    # Bat
    draw.rounded_rectangle(
        (
            cx + 160,
            cy - 280,
            cx + 260,
            cy + 260
        ),
        radius=20,
        fill=brown,
        outline="white",
        width=5
    )

    draw.line(
        (
            cx + 210,
            cy + 250,
            cx + 210,
            cy + 430
        ),
        fill=brown,
        width=55
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

    water_top = 800

    draw.rectangle(
        (
            0,
            water_top,
            width,
            height
        ),
        fill=(
            10,
            120,
            195
        )
    )

    # Sun
    draw.ellipse(
        (
            800,
            180,
            980,
            360
        ),
        fill=(
            255,
            205,
            50
        )
    )

    # Waves
    for y in range(
        water_top + 60,
        height,
        120
    ):

        for x in range(
            -100,
            width + 100,
            220
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
                width=6
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
        155,
        235
    )

    r = 230

    draw.ellipse(
        (
            cx - r,
            cy - r,
            cx + r,
            cy + r
        ),
        fill=blue,
        outline="white",
        width=8
    )

    # Longitude
    draw.ellipse(
        (
            cx - 100,
            cy - r,
            cx + 100,
            cy + r
        ),
        outline="white",
        width=6
    )

    # Latitude
    draw.arc(
        (
            cx - r,
            cy - 120,
            cx + r,
            cy + 120
        ),
        0,
        360,
        fill="white",
        width=6
    )

    # Equator
    draw.line(
        (
            cx - r,
            cy,
            cx + r,
            cy
        ),
        fill="white",
        width=6
    )


# ============================================================
# VISUAL ROUTER
# ============================================================

def draw_visual(
    draw,
    visual,
    width,
    height,
    frame=0
):

    cx = width // 2
    cy = int(height * 0.40)

    visual = str(
        visual
    ).lower().strip()

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
                cx - 180,
                cy - 180,
                cx + 180,
                cy + 180
            ),
            fill=(
                70,
                140,
                200
            ),
            outline="white",
            width=8
        )


# ============================================================
# CREATE IMAGE
# ============================================================

def create_image(content):

    IMAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    content_id = content.get(
        "content_id",
        content.get(
            "id",
            "content"
        )
    )

    category = content.get(
        "category",
        "general"
    )

    visual = content.get(
        "visual",
        category
    )

    image = create_background(
        category,
        IMAGE_WIDTH,
        IMAGE_HEIGHT
    )

    draw = ImageDraw.Draw(image)

    # Visual
    draw_visual(
        draw,
        visual,
        IMAGE_WIDTH,
        IMAGE_HEIGHT
    )

    # Fonts
    title_font = get_font(70)
    fact_font = get_font(48)
    footer_font = get_font(38)

    # Title
    draw_center_text(
        draw,
        content.get(
            "title",
            ""
        ),
        780,
        title_font,
        IMAGE_WIDTH,
        IMAGE_WIDTH - 100
    )

    # Fact
    draw_center_text(
        draw,
        content.get(
            "fact",
            ""
        ),
        950,
        fact_font,
        IMAGE_WIDTH,
        IMAGE_WIDTH - 120
    )

    # Page
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
        / f"{content_id}.png"
    )

    image.save(
        output,
        "PNG"
    )

    print(
        f"[IMAGE] Created: {output}"
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

    content_id = content.get(
        "content_id",
        content.get(
            "id",
            "content"
        )
    )

    category = content.get(
        "category",
        "general"
    )

    visual = content.get(
        "visual",
        category
    )

    frames_dir = (
        REEL_DIR
        / f"{content_id}_frames"
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
        f"[REEL] Creating {total_frames} frames..."
    )

    for frame_number in range(
        total_frames
    ):

        image = create_background(
            category,
            REEL_WIDTH,
            REEL_HEIGHT,
            frame_number
        )

        draw = ImageDraw.Draw(image)

        # Exact visual
        draw_visual(
            draw,
            visual,
            REEL_WIDTH,
            REEL_HEIGHT,
            frame_number
        )

        # Small animation
        movement = int(
            math.sin(
                frame_number / 15
            ) * 20
        )

        # Title
        draw_center_text(
            draw,
            content.get(
                "title",
                ""
            ),
            130 + movement,
            title_font,
            REEL_WIDTH,
            REEL_WIDTH - 100
        )

        # Fact
        draw_center_text(
            draw,
            content.get(
                "fact",
                ""
            ),
            1050,
            fact_font,
            REEL_WIDTH,
            REEL_WIDTH - 120
        )

        # Question / CTA
        question = content.get(
            "question",
            "ඔබේ අදහස Comment කරන්න! 💬"
        )

        draw_center_text(
            draw,
            question,
            1500,
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
        / f"{content_id}.mp4"
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
        "[REEL] Rendering MP4..."
    )

    subprocess.run(
        command,
        check=True
    )

    print(
        f"[REEL] Created: {output}"
    )

    return output
