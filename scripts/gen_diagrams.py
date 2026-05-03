#!/usr/bin/env python3
"""Generates three architecture diagram PNGs for Belpro_Architecture.docx.

Output: scripts/diagrams/fig1_architecture.png
        scripts/diagrams/fig2_workflow.png
        scripts/diagrams/fig3_reporting.png

Each image is 940 px wide (= A4 content width at 150 DPI).
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ── Palette ──────────────────────────────────────────────────────────────────
TEAL_DARK  = (26, 107, 107)
TEAL_MID   = (46, 139, 139)
ORANGE     = (200, 100, 15)
ORANGE2    = (180, 88, 5)
GREEN_BOX  = (34, 120, 75)
BLUE_BOX   = (34, 100, 160)
GRAY_BOX   = (90, 120, 120)
WHITE      = (255, 255, 255)
LIGHT_BG   = (248, 252, 252)
ARROW_COL  = (90, 90, 90)
DASHED_COL = (110, 165, 165)
DOUBLE_COL = (0, 100, 100)
SUB_TEXT   = (200, 235, 235)

W = 940   # full content width (A4 – 2×1 inch margins at 150 DPI)

FONT_REG  = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"


def fnt(size, bold=False):
    try:
        return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)
    except OSError:
        return ImageFont.load_default()


def text_size(font, text):
    """Return (width, height) of text string."""
    bb = font.getbbox(text)
    return bb[2] - bb[0], bb[3] - bb[1]


def draw_box(draw, x, y, w, h, fill, title, subtitle="", r=10):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill)
    ft = fnt(14, bold=True)
    fs = fnt(11)
    tw, th = text_size(ft, title)
    if subtitle:
        sw, sh = text_size(fs, subtitle)
        total = th + 5 + sh
        ty = y + (h - total) // 2
        draw.text((x + (w - tw) // 2, ty), title, fill=WHITE, font=ft)
        draw.text((x + (w - sw) // 2, ty + th + 5), subtitle, fill=SUB_TEXT, font=fs)
    else:
        draw.text((x + (w - tw) // 2, y + (h - th) // 2), title, fill=WHITE, font=ft)


def arrow_h(draw, x1, x2, y, color=ARROW_COL, width=2):
    draw.line([(x1, y), (x2, y)], fill=color, width=width)
    draw.polygon([(x2, y), (x2 - 9, y - 4), (x2 - 9, y + 4)], fill=color)


def arrow_v(draw, x, y1, y2, color=ARROW_COL, width=2, dashed=False):
    if dashed:
        seg, gap, cy = 8, 5, y1
        while cy < y2:
            draw.line([(x, cy), (x, min(cy + seg, y2))], fill=color, width=width)
            cy += seg + gap
    else:
        draw.line([(x, y1), (x, y2)], fill=color, width=width)
    draw.polygon([(x, y2), (x - 4, y2 - 9), (x + 4, y2 - 9)], fill=color)


def arrow_h_dashed(draw, x1, x2, y, color=DOUBLE_COL, width=2):
    seg, gap, cx = 10, 5, x1
    while cx < x2 - 9:
        draw.line([(cx, y - 1), (min(cx + seg, x2 - 9), y - 1)], fill=color, width=width)
        draw.line([(cx, y + 1), (min(cx + seg, x2 - 9), y + 1)], fill=color, width=width)
        cx += seg + gap
    draw.polygon([(x2, y), (x2 - 9, y - 5), (x2 - 9, y + 5)], fill=color)


def arrow_h_dotted(draw, x1, x2, y, color=DASHED_COL, width=2):
    """Dashed horizontal arrow (single line, for Manager connection)."""
    seg, gap, cx = 8, 6, x1
    while cx < x2 - 9:
        draw.line([(cx, y), (min(cx + seg, x2 - 9), y)], fill=color, width=width)
        cx += seg + gap
    draw.polygon([(x2, y), (x2 - 9, y - 4), (x2 - 9, y + 4)], fill=color)


# ── Fig 1: Architecture diagram ───────────────────────────────────────────────
def fig1():
    H = 285
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)

    BW = 122; BH = 64

    # Column centres
    CA = 80;  CB = 248;  CC = 428;  CD = 608;  CE = 822
    # Row top-y
    R1Y = 38;  R2Y = 185

    # Row 1 boxes
    draw_box(d, CA - BW//2, R1Y, BW, BH, TEAL_DARK, "Volunteer",    "WhatsApp")
    draw_box(d, CB - BW//2, R1Y, BW, BH, TEAL_DARK, "Evolution API","API Gateway")
    draw_box(d, CC - BW//2, R1Y, BW, BH, TEAL_DARK, "n8n",          "Workflow Engine")
    draw_box(d, CD - BW//2, R1Y, BW, BH, ORANGE,    "Dashboard",    "Web UI + API")

    # Manager (smaller, top-right)
    MW = 100; MH = 54
    draw_box(d, CE - MW//2, R1Y + 5, MW, MH, GRAY_BOX, "Manager", "Browser / Phone", r=8)

    # Row 2 boxes
    draw_box(d, CB - BW//2, R2Y, BW, BH, GRAY_BOX,  "Whisper AI",  "Transcription")
    draw_box(d, CC - BW//2, R2Y, BW, BH, TEAL_DARK, "PostgreSQL",  "Database")
    draw_box(d, CD - BW//2, R2Y, BW, BH, GREEN_BOX, "Gmail",       "Email Delivery")

    # Row 1 horizontal arrows
    R1CY = R1Y + BH // 2
    arrow_h(d, CA + BW//2, CB - BW//2 - 3, R1CY)
    arrow_h(d, CB + BW//2, CC - BW//2 - 3, R1CY)
    arrow_h(d, CC + BW//2, CD - BW//2 - 3, R1CY)

    # Dashboard → Manager (dashed horizontal)
    arrow_h_dotted(d, CD + BW//2, CE - MW//2 - 3, R1CY)

    # Vertical arrows
    arrow_v(d, CB, R1Y + BH, R2Y - 3, color=DASHED_COL, dashed=True)  # Evolution ··· Whisper
    arrow_v(d, CC, R1Y + BH, R2Y - 3, color=ARROW_COL)                 # n8n → PostgreSQL

    # Row 2 horizontal arrows
    R2CY = R2Y + BH // 2
    arrow_h(d, CB + BW//2, CC - BW//2 - 3, R2CY)          # Whisper → PostgreSQL
    arrow_h_dashed(d, CC + BW//2, CD - BW//2 - 3, R2CY)   # PostgreSQL ═══ Gmail

    # Legend (bottom-left)
    fl = fnt(10)
    ly = H - 18
    arrow_h(d, 18, 40, ly, color=ARROW_COL)
    d.text((46, ly - 7), "Data flow", fill=(110, 110, 110), font=fl)
    arrow_v(d, 130, ly - 6, ly + 2, color=DASHED_COL, dashed=True)
    d.text((139, ly - 7), "AI-assisted", fill=(110, 110, 110), font=fl)
    arrow_h_dashed(d, 230, 258, ly, color=DOUBLE_COL)
    d.text((264, ly - 7), "Sync", fill=(110, 110, 110), font=fl)

    return img


# ── Fig 2: Five-step volunteer workflow ───────────────────────────────────────
def fig2():
    H = 150
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)

    PAD = 14; AW = 28; N = 5
    BW = (W - 2 * PAD - (N - 1) * AW) // N
    BH = H - 2 * PAD

    colours = [TEAL_DARK, TEAL_MID, ORANGE, ORANGE2, GREEN_BOX]
    steps = [
        ("① Record",     "Voice note\n+ optional photo"),
        ("② AI Cleans",  "Whisper transcribes\ndialect normalised"),
        ("③ Confirm",    "Volunteer reviews\napproves / edits"),
        ("④ Manager OK", "Manager approves\nvia WhatsApp"),
        ("⑤ Done",       "Entry saved\nvolunteer notified"),
    ]

    ft = fnt(13, bold=True)
    fs = fnt(10)

    for i, (title, sub) in enumerate(steps):
        bx = PAD + i * (BW + AW)
        by = PAD
        d.rounded_rectangle([bx, by, bx + BW, by + BH], radius=8, fill=colours[i])

        tw, th = text_size(ft, title)
        lines = sub.split("\n")
        line_h = [text_size(fs, l) for l in lines]
        total_sub_h = sum(lh[1] for lh in line_h) + 3 * (len(lines) - 1)
        total_h = th + 7 + total_sub_h
        ty = by + (BH - total_h) // 2

        d.text((bx + (BW - tw) // 2, ty), title, fill=WHITE, font=ft)
        yo = ty + th + 7
        for j, line in enumerate(lines):
            lw = line_h[j][0]
            lhh = line_h[j][1]
            d.text((bx + (BW - lw) // 2, yo), line, fill=SUB_TEXT, font=fs)
            yo += lhh + 3

        if i < N - 1:
            ax = bx + BW + 3; ae = bx + BW + AW - 3; ay = by + BH // 2
            d.line([(ax, ay), (ae, ay)], fill=(110, 140, 140), width=2)
            d.polygon([(ae, ay), (ae - 7, ay - 3), (ae - 7, ay + 3)], fill=(110, 140, 140))

    return img


# ── Fig 3: Monthly reporting cycle ────────────────────────────────────────────
def fig3():
    H = 138
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)

    PAD = 14; AW = 32; N = 4
    BW = (W - 2 * PAD - (N - 1) * AW) // N
    BH = H - 2 * PAD

    colours = [TEAL_DARK, TEAL_MID, ORANGE, BLUE_BOX]
    steps = [
        ("28th of Month",  "Automatic trigger"),
        ("PDF Generated",  "Per volunteer\n+ consolidated"),
        ("Email Sent",     "To volunteer\n& manager"),
        ("CSD Submission", "Volunteer signs\n& submits"),
    ]

    ft = fnt(13, bold=True)
    fs = fnt(10)

    for i, (title, sub) in enumerate(steps):
        bx = PAD + i * (BW + AW)
        by = PAD
        d.rounded_rectangle([bx, by, bx + BW, by + BH], radius=8, fill=colours[i])

        tw, th = text_size(ft, title)
        lines = sub.split("\n")
        line_h = [text_size(fs, l) for l in lines]
        total_sub_h = sum(lh[1] for lh in line_h) + 3 * (len(lines) - 1)
        total_h = th + 7 + total_sub_h
        ty = by + (BH - total_h) // 2

        d.text((bx + (BW - tw) // 2, ty), title, fill=WHITE, font=ft)
        yo = ty + th + 7
        for j, line in enumerate(lines):
            lw = line_h[j][0]
            lhh = line_h[j][1]
            d.text((bx + (BW - lw) // 2, yo), line, fill=SUB_TEXT, font=fs)
            yo += lhh + 3

        if i < N - 1:
            ax = bx + BW + 3; ae = bx + BW + AW - 3; ay = by + BH // 2
            d.line([(ax, ay), (ae, ay)], fill=(110, 140, 140), width=2)
            d.polygon([(ae, ay), (ae - 7, ay - 3), (ae - 7, ay + 3)], fill=(110, 140, 140))

    return img


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    out = os.path.join(os.path.dirname(__file__), "diagrams")
    os.makedirs(out, exist_ok=True)
    for name, fn in [
        ("fig1_architecture", fig1),
        ("fig2_workflow",     fig2),
        ("fig3_reporting",    fig3),
    ]:
        img = fn()
        path = os.path.join(out, f"{name}.png")
        img.save(path, "PNG", dpi=(150, 150))
        print(f"Written: {path}  ({img.size[0]}×{img.size[1]})")


if __name__ == "__main__":
    main()
