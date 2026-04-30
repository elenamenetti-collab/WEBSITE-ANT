#!/usr/bin/env python3
"""
Video: 10 anni di Ant Capital
Genera un video MP4 celebrativo per LinkedIn (1920x1080, ~60s, 25fps)
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import ImageClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut
import os

# ── Costanti ──────────────────────────────────────────────────────────────────
W, H  = 1920, 1080
FPS   = 25
NAVY  = (3, 20, 48)          # #031430
GOLD  = (212, 183, 104)      # #d4b768
WHITE = (255, 255, 255)
LIGHT = (230, 233, 240)

BASE  = "G:/Drive condivisi/Server CF/2.1 Ideas/0. Pjt Interno/4. Website/WEBSITE-ANT"
OUT   = "G:/Drive condivisi/Server CF/2.1 Ideas/0. Pjt Interno/Video/ant_capital_10anni.mp4"

# ── Font ──────────────────────────────────────────────────────────────────────
FONT_BOLD   = "C:/Windows/Fonts/georgiab.ttf"
FONT_LIGHT  = "C:/Windows/Fonts/georgia.ttf"

def fb(size):
    return ImageFont.truetype(FONT_BOLD, size)

def fl(size):
    return ImageFont.truetype(FONT_LIGHT, size)

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_logo(filename, height):
    path = os.path.join(BASE, "Loghi", filename)
    img = Image.open(path).convert("RGBA")
    w = int(img.width * height / img.height)
    return img.resize((w, height), Image.LANCZOS)

def paste(bg, overlay, cx, cy):
    x = cx - overlay.width // 2
    y = cy - overlay.height // 2
    if overlay.mode == "RGBA":
        bg.paste(overlay, (x, y), overlay)
    else:
        bg.paste(overlay, (x, y))

def gold_bar(draw, y, width=360):
    x = (W - width) // 2
    draw.rectangle([(x, y), (x + width, y + 4)], fill=GOLD)

def borders(draw, bg_color):
    """Top/bottom gold accent lines"""
    draw.rectangle([(0, 0), (W, 7)], fill=GOLD)
    draw.rectangle([(0, H - 7), (W, H)], fill=GOLD)

# ── Slide 1 — Titolo ──────────────────────────────────────────────────────────
def slide_title():
    img = Image.new("RGB", (W, H), WHITE)
    d   = ImageDraw.Draw(img)
    borders(d, WHITE)
    d.rectangle([(0, 0), (7, H)], fill=NAVY)   # navy left bar

    logo = load_logo("AntCapital-SfondoBiancoA-Logo.png", 190)
    paste(img, logo, W // 2, 260)

    d.text((W // 2, 450), "10 anni di", font=fl(76), fill=NAVY, anchor="mm")
    d.text((W // 2, 600), "ANT CAPITAL", font=fb(148), fill=NAVY, anchor="mm")
    gold_bar(d, 690, 500)
    d.text((W // 2, 760), "2016  —  2026", font=fl(58), fill=GOLD, anchor="mm")
    d.text((W // 2, 870), "Investment Banking  ·  M&A Advisory  ·  Milano",
           font=fl(36), fill=(90, 100, 120), anchor="mm")
    return img

# ── Slide 2 — Chi siamo ───────────────────────────────────────────────────────
def slide_about():
    img = Image.new("RGB", (W, H), WHITE)
    d   = ImageDraw.Draw(img)
    borders(d, WHITE)
    d.rectangle([(0, 0), (7, H)], fill=NAVY)

    d.text((W // 2, 140), "CHI SIAMO", font=fb(54), fill=GOLD, anchor="mm")
    gold_bar(d, 185, 180)

    lines = [
        "Boutique indipendente specializzata in",
        "Mergers & Acquisitions, Capital Raising",
        "e Advisory Strategico",
    ]
    for i, line in enumerate(lines):
        d.text((W // 2, 320 + i * 100), line, font=fl(62), fill=NAVY, anchor="mm")

    gold_bar(d, 640, 500)

    d.text((W // 2, 720), "per le aziende mid-market",
           font=fl(54), fill=(80, 90, 110), anchor="mm")
    d.text((W // 2, 800), "italiane e internazionali",
           font=fl(54), fill=(80, 90, 110), anchor="mm")

    d.text((W // 2, 940), "Indipendenza  ·  Eccellenza  ·  Riservatezza",
           font=fl(38), fill=GOLD, anchor="mm")
    return img

# ── Slide 3 — Numeri ──────────────────────────────────────────────────────────
def slide_numbers():
    img = Image.new("RGB", (W, H), WHITE)
    d   = ImageDraw.Draw(img)
    borders(d, WHITE)
    d.rectangle([(0, 0), (7, H)], fill=NAVY)

    d.text((W // 2, 140), "TRACK RECORD", font=fb(54), fill=GOLD, anchor="mm")
    gold_bar(d, 185, 200)

    d.text((W // 2, 420), "22+", font=fb(240), fill=NAVY, anchor="mm")
    d.text((W // 2, 590), "Transazioni Advisory", font=fl(70), fill=NAVY, anchor="mm")
    gold_bar(d, 660, 500)

    services = "M&A  ·  Debt Advisory  ·  Financial Advisory  ·  Private Placement"
    d.text((W // 2, 750), services, font=fl(42), fill=GOLD, anchor="mm")
    d.text((W // 2, 880), "Dal 2016 al 2025", font=fl(40), fill=(90, 100, 120), anchor="mm")
    return img

# ── Slide 4 — Operazioni ──────────────────────────────────────────────────────
def slide_deals():
    img = Image.new("RGB", (W, H), WHITE)
    d   = ImageDraw.Draw(img)
    borders(d, WHITE)
    d.rectangle([(0, 0), (7, H)], fill=NAVY)

    d.text((W // 2, 72), "ALCUNE DELLE NOSTRE OPERAZIONI",
           font=fb(46), fill=NAVY, anchor="mm")
    d.rectangle([(W // 2 - 440, 112), (W // 2 + 440, 116)], fill=GOLD)

    # Divisore verticale
    d.line([(W // 2, 130), (W // 2, H - 30)], fill=LIGHT, width=2)

    deals_l = [
        ("2025", "Dream Flower / Xerjoff"),
        ("2025", "Venpa / Euronoleggi"),
        ("2025", "Quantyca / Jakala"),
        ("2024", "Parallelozero / Valica"),
        ("2022", "Private Investors / Slitti"),
        ("2021", "Lombarda Acciai"),
    ]
    deals_r = [
        ("2020", "Beintoo / Mediaset"),
        ("2019", "Univergomma / Overgom"),
        ("2018", "Gruppo Flema / Bridgestone"),
        ("2018", "Futuris Isontina / Motus Energy"),
        ("2017", "Innovando / Dafne"),
        ("2016", "Supermercato24"),
    ]

    def draw_deal_list(deals, col_x):
        y0, dy = 148, 120
        for i, (year, name) in enumerate(deals):
            y = y0 + i * dy
            # Year badge
            d.rounded_rectangle([(col_x, y), (col_x + 88, y + 42)],
                                 radius=5, fill=NAVY)
            d.text((col_x + 44, y + 21), year, font=fb(26), fill=GOLD, anchor="mm")
            d.text((col_x + 106, y + 21), name, font=fl(36), fill=NAVY, anchor="lm")
            d.line([(col_x, y + 58), (col_x + 800, y + 58)], fill=LIGHT, width=1)

    draw_deal_list(deals_l, 60)
    draw_deal_list(deals_r, W // 2 + 40)
    return img

# ── Slide 5 — Team ────────────────────────────────────────────────────────────
def slide_team():
    img = Image.new("RGB", (W, H), WHITE)
    d   = ImageDraw.Draw(img)
    borders(d, WHITE)
    d.rectangle([(0, 0), (7, H)], fill=NAVY)

    d.text((W // 2, 80), "IL NOSTRO TEAM", font=fb(56), fill=NAVY, anchor="mm")
    gold_bar(d, 128, 200)

    team = [
        ("Antonio Urselli",                "Managing Director & Founder"),
        ("Filippo Privitera",              "Non Executive Partner"),
        ("Daniele Sabato",                 "Non Executive Partner"),
        ("Stefano De Pascale",             "Director"),
        ("Alessandro Serati",              "Associate"),
        ("Sergiu Denis Lazar",             "Analyst"),
        ("Luca Gennaro",                   "Analyst"),
        ("Mauro Brunelli",                 "Senior Advisor"),
        ("Gherardo Laffineur Petracchini", "Advisory Board Member"),
        ("Giovanni Grasso",                "Advisory Board Member"),
    ]

    col_w  = W // 2
    row_h  = (H - 195) // 5

    for i, (name, role) in enumerate(team):
        col = i % 2
        row = i // 2
        cx  = col * col_w + col_w // 2 + 20
        cy  = 185 + row * row_h + row_h // 2

        d.text((cx, cy - 22), name, font=fb(36), fill=NAVY, anchor="mm")
        d.text((cx, cy + 22), role, font=fl(28), fill=GOLD, anchor="mm")

        if col == 0:
            d.line([(col_w // 4, cy + 50), (col_w * 3 // 4, cy + 50)],
                   fill=LIGHT, width=1)
        else:
            d.line([(W // 2 + col_w // 4, cy + 50), (W // 2 + col_w * 3 // 4, cy + 50)],
                   fill=LIGHT, width=1)

    return img

# ── Slide 6 — Chiusura ────────────────────────────────────────────────────────
def slide_closing():
    img = Image.new("RGB", (W, H), NAVY)
    d   = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (W, 7)], fill=GOLD)
    d.rectangle([(0, H - 7), (W, H)], fill=GOLD)

    logo = load_logo("Logo_Ant-Capital_Pay-off_bianco.png", 160)
    paste(img, logo, W // 2, 210)

    gold_bar(d, 305, 400)

    d.text((W // 2, 430), "Grazie a tutti coloro che", font=fl(76), fill=WHITE, anchor="mm")
    d.text((W // 2, 540), "hanno creduto in noi", font=fl(76), fill=WHITE, anchor="mm")

    gold_bar(d, 610, 400)

    d.text((W // 2, 710), "in questi 10 anni di avventura",
           font=fl(60), fill=GOLD, anchor="mm")

    d.text((W // 2, 900), "antcapital.it", font=fl(44), fill=GOLD, anchor="mm")
    return img

# ── Assembla il video ─────────────────────────────────────────────────────────
def to_clip(img, duration, fi=0.8, fo=0.8):
    arr  = np.array(img)
    clip = ImageClip(arr, duration=duration)
    clip = clip.with_effects([FadeIn(fi), FadeOut(fo)])
    return clip

def main():
    print("Generazione slide...")
    slides = [
        (slide_title(),   10),
        (slide_about(),    8),
        (slide_numbers(),  9),
        (slide_deals(),   12),
        (slide_team(),    10),
        (slide_closing(), 11),
    ]

    clips = [to_clip(img, dur) for img, dur in slides]
    final = concatenate_videoclips(clips, method="compose")

    print(f"Rendering video -> {OUT}")
    final.write_videofile(OUT, fps=FPS, codec="libx264", audio=False, logger="bar")
    print(f"\nVideo pronto: {OUT}")

if __name__ == "__main__":
    main()
