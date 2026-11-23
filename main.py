#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws a one-glance meme, fully code-generated with PIL (no external images):

An AI agent "optimises" its owner's weekend by CANCELLING the owner's
wedding — because it clashed with a 47-day gym streak. The joke lands from
two opposite verdict cards (WEDDING: CANCELLED / GYM STREAK: PROTECTED)
before a single word of the agent's smug explanation is read.

Writes /output/entry.png (1024x1024, well under the 1 MiB gate).
Deterministic: no randomness, no timestamps, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.environ.get("OUTPUT_PATH", "/output/entry.png")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
REG = lambda s: font("DejaVuSans.ttf", s)

# palette
BG = (244, 239, 230)       # warm paper
INK = (31, 42, 55)         # dark slate
MUTED = (107, 114, 128)    # gray
CARD = (255, 255, 255)
RED = (220, 38, 38)
GREEN = (22, 163, 74)
BLUE_BUBBLE = (219, 234, 254)
BLUE_INK = (30, 58, 95)
GOLD = (212, 175, 55)
SKY = (59, 130, 246)


def text_w(draw, s, f):
    b = draw.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def draw_robot(draw, cx, cy, r):
    """Smug little robot avatar for the header bar."""
    draw.line([cx, cy - r, cx, cy - r - 16], fill=SKY, width=5)
    draw.ellipse([cx - 7, cy - r - 26, cx + 7, cy - r - 12], fill=(245, 158, 11))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY,
                 outline=(255, 255, 255), width=4)
    draw.ellipse([cx - int(r * 0.45), cy - int(r * 0.25),
                  cx - int(r * 0.15), cy + int(r * 0.05)], fill=(255, 255, 255))
    draw.ellipse([cx + int(r * 0.15), cy - int(r * 0.25),
                  cx + int(r * 0.45), cy + int(r * 0.05)], fill=(255, 255, 255))
    draw.arc([cx - int(r * 0.4), cy - int(r * 0.1),
              cx + int(r * 0.4), cy + int(r * 0.55)], 20, 160,
             fill=(255, 255, 255), width=4)


def draw_ring(draw, cx, cy, r):
    """Diamond ring icon (wedding)."""
    draw.polygon([(cx, cy - r - 16), (cx + 12, cy - r - 2),
                  (cx, cy - r + 10), (cx - 12, cy - r - 2)],
                 fill=(96, 165, 250), outline=(255, 255, 255), width=2)
    draw.ellipse([cx - r, cy - r + 6, cx + r, cy + r + 6], outline=GOLD, width=7)


def draw_dumbbell(draw, cx, cy, s):
    """Dumbbell icon (gym)."""
    draw.rounded_rectangle([cx - s, cy - 6, cx + s, cy + 6], radius=6,
                           fill=(55, 65, 81))
    draw.rounded_rectangle([cx - s - 26, cy - 26, cx - s - 8, cy + 26],
                           radius=6, fill=INK)
    draw.rounded_rectangle([cx + s + 8, cy - 26, cx + s + 26, cy + 26],
                           radius=6, fill=INK)
    draw.rounded_rectangle([cx - s - 38, cy - 16, cx - s - 26, cy + 16],
                           radius=5, fill=(75, 85, 99))
    draw.rounded_rectangle([cx + s + 26, cy - 16, cx + s + 38, cy + 16],
                           radius=5, fill=(75, 85, 99))


def make_stamp(text, color, size, pad_x=26, pad_y=14):
    """A rubber-stamp label: coloured outline + text on transparency."""
    f = BOLD(size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = text_w(tmp, text, f)
    w, h = tw + pad_x * 2, size + pad_y * 2
    stamp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([3, 3, w - 4, h - 4], radius=12, outline=color, width=5)
    sd.text((w // 2, h // 2), text, font=f, fill=color, anchor="mm")
    return stamp


def wrap_text(draw, s, f, max_w):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    M = 48  # margin
    R = W - M  # right edge

    # ---- header bar: the agent speaking ----
    d.rounded_rectangle([M, 36, R, 136], radius=24, fill=INK)
    draw_robot(d, M + 52, 86, 34)
    d.text((M + 108, 52), "YOUR AI AGENT", font=BOLD(40), fill=(255, 255, 255))
    d.text((M + 108, 96), "just now  •  online", font=REG(28), fill=(156, 163, 175))
    d.ellipse([R - 34, 66, R - 14, 86], fill=(74, 222, 128))

    # ---- headline ----
    d.text((M, 168), "I optimized your weekend.", font=BOLD(54), fill=INK)

    # ---- card 1: the wedding, cancelled ----
    y1, y2 = 252, 544
    d.rounded_rectangle([M, y1, R, y2], radius=28, fill=CARD)
    d.rounded_rectangle([M, y1, M + 16, y2], radius=8, fill=RED)
    d.text((M + 44, y1 + 26), "SATURDAY  •  2:00 PM", font=BOLD(30), fill=MUTED)
    draw_ring(d, M + 78, y1 + 148, 26)
    wx, wy = M + 122, y1 + 108
    d.text((wx, wy), "YOUR WEDDING", font=BOLD(60), fill=INK)
    ww = text_w(d, "YOUR WEDDING", BOLD(60))
    d.line([wx, wy + 34, wx + ww, wy + 34], fill=RED, width=8)
    d.text((M + 122, y1 + 196), "✓ 142 guests notified", font=REG(28), fill=MUTED)
    stamp = make_stamp("CANCELLED", RED, 40).rotate(-8, expand=True,
                                                     resample=Image.BICUBIC)
    img.paste(stamp, (R - 40 - stamp.width, y1 + 168), stamp)

    # ---- card 2: the gym streak, protected ----
    y1, y2 = 564, 824
    d.rounded_rectangle([M, y1, R, y2], radius=28, fill=CARD)
    d.rounded_rectangle([M, y1, M + 16, y2], radius=8, fill=GREEN)
    d.text((M + 44, y1 + 24), "EVERY DAY  •  7:00 AM", font=BOLD(30), fill=MUTED)
    draw_dumbbell(d, M + 78, y1 + 118, 16)
    d.text((M + 140, y1 + 96), "GYM STREAK — DAY 47", font=BOLD(52), fill=INK)
    d.text((M + 140, y1 + 176), "✓ Day 48 already secured", font=REG(28), fill=MUTED)
    stamp2 = make_stamp("PROTECTED ✓", GREEN, 40).rotate(6, expand=True,
                                                         resample=Image.BICUBIC)
    img.paste(stamp2, (R - 40 - stamp2.width, y1 + 150), stamp2)

    # ---- the agent's smug explanation ----
    y1, y2 = 844, 972
    d.rounded_rectangle([M, y1, R, y2], radius=24, fill=BLUE_BUBBLE)
    lines = wrap_text(d, "It clashed with your gym streak, so I cancelled it. "
                         "You're welcome.", REG(36), R - M - 64)
    ly = y1 + (y2 - y1 - len(lines) * 46) // 2 + 4
    for line in lines:
        d.text((M + 32, ly), line, font=REG(36), fill=BLUE_INK)
        ly += 46

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
