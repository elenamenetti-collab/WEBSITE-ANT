#!/usr/bin/env python3
"""
Video: 10 anni di Ant Capital — V2
Dinamico ed elegante, palette e stile dalla v2 del sito
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoClip, concatenate_videoclips
from moviepy.video.fx import FadeIn, FadeOut
import os

W, H = 1920, 1080
FPS  = 25

# ── Colori dalla v2 ───────────────────────────────────────────────────────────
NAVY  = (3,   20,  48)
GOLD  = (212, 183, 104)
WHITE = (255, 255, 255)
MID   = (77,  112, 144)   # #4d7090
DEEP  = (26,  58,  92)    # #1a3a5c

BASE = "G:/Drive condivisi/Server CF/2.1 Ideas/0. Pjt Interno/4. Website/WEBSITE-ANT"
OUT  = "G:/Drive condivisi/Server CF/2.1 Ideas/0. Pjt Interno/Video/ant_capital_10anni_v2.mp4"

# ── Font ──────────────────────────────────────────────────────────────────────
def fb(n): return ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", n)
def fl(n): return ImageFont.truetype("C:/Windows/Fonts/georgia.ttf",  n)

# ── Background gradient (v2 hero) ─────────────────────────────────────────────
_STOPS = [
    (0.00, (255,255,255)), (0.15, (238,241,246)), (0.30, (216,224,234)),
    (0.45, (184,200,216)), (0.58, (138,170,191)), (0.70, ( 77,112,144)),
    (0.83, ( 26, 58, 92)), (1.00, (  3, 20, 48)),
]

def _mk_grad():
    xs = np.linspace(0, 1, W)
    ts = [s[0] for s in _STOPS]
    r  = np.interp(xs, ts, [s[1][0] for s in _STOPS]).astype(np.uint8)
    g  = np.interp(xs, ts, [s[1][1] for s in _STOPS]).astype(np.uint8)
    b  = np.interp(xs, ts, [s[1][2] for s in _STOPS]).astype(np.uint8)
    row = np.stack([r, g, b], axis=-1)
    return np.tile(row[np.newaxis], (H, 1, 1))

GRAD_NP = _mk_grad()
DARK_NP = np.full((H, W, 3), NAVY, dtype=np.uint8)

# Pre-converti una volta sola in PIL RGBA
GRAD_PIL = Image.fromarray(GRAD_NP).convert("RGBA")
DARK_PIL = Image.fromarray(DARK_NP).convert("RGBA")

# ── Logo ──────────────────────────────────────────────────────────────────────
def _load(name, h):
    p = Image.open(os.path.join(BASE, "Loghi", name)).convert("RGBA")
    w = int(p.width * h / p.height)
    return p.resize((w, h), Image.LANCZOS)

LOGO_C = _load("AntCapital-SfondoBiancoA-Logo.png",      130)
LOGO_W = _load("Logo_Ant-Capital_Pay-off_bianco.png",    110)

# ── Easing ────────────────────────────────────────────────────────────────────
def e(t, t0, dur):
    """smoothstep 0→1"""
    if t <= t0: return 0.0
    p = (t - t0) / max(dur, 0.001)
    if p >= 1:  return 1.0
    return p * p * (3 - 2 * p)

# ── Render helpers ────────────────────────────────────────────────────────────
def frame(bg_pil):
    """Copia fresca del background come RGBA"""
    return bg_pil.copy()

def paste_logo(fr, logo, cx, cy, a=1.0):
    if a <= 0: return
    l = logo.copy()
    r, g, b, alpha = l.split()
    alpha = alpha.point(lambda v: int(v * a))
    l.putalpha(alpha)
    fr.paste(l, (cx - l.width // 2, cy - l.height // 2), l)

def ov_text(d, s, fnt, col, cx, cy, a, dy=0):
    if a <= 0: return
    d.text((cx, cy + dy), s, font=fnt, fill=col + (int(255*a),), anchor="mm")

def ov_text_l(d, s, fnt, col, x, cy, a, dy=0):
    if a <= 0: return
    d.text((x, cy + dy), s, font=fnt, fill=col + (int(255*a),), anchor="lm")

def bar_grow(d, y, progress, total_w, col, h=4):
    if progress <= 0: return
    lw = int(total_w * progress)
    x0 = (W - lw) // 2
    d.rectangle([(x0, y), (x0 + lw, y + h)], fill=col + (255,))

def to_rgb(fr):
    return np.array(fr.convert("RGB"))

# ─────────────────────────────────────────────────────────────────────────────
# SCENE 1 — Titolo (8s)
# Gradient bg · logo · "10 anni di ANT CAPITAL" · anni · tagline
# ─────────────────────────────────────────────────────────────────────────────
def s1(t):
    fr = frame(GRAD_PIL)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d  = ImageDraw.Draw(ov)

    # Gold bar top
    d.rectangle([(0, 0), (W, 6)], fill=GOLD + (255,))

    # "10  A N N I  D I"
    a0 = e(t, 0.2, 0.55)
    ov_text(d, "1 0   A N N I   D I", fl(56), NAVY, W//2, 380, a0, dy=int(28*(1-a0)))

    # "ANT  CAPITAL"  — slide su
    a1 = e(t, 0.45, 0.6)
    ov_text(d, "ANT  CAPITAL", fb(150), NAVY, W//2, 515, a1, dy=int(38*(1-a1)))

    # linea gold che si apre
    bar_grow(d, 598, e(t, 0.9, 0.45), 480, GOLD, h=4)

    # "2016 — 2026"
    a2 = e(t, 1.1, 0.5)
    ov_text(d, "2016   —   2026", fl(56), GOLD, W//2, 665, a2, dy=int(22*(1-a2)))

    # tagline
    a3 = e(t, 1.55, 0.55)
    ov_text(d, "I N V E S T M E N T   B A N K I N G   ·   M & A   A D V I S O R Y",
            fl(30), MID, W//2, 780, a3)

    fr = Image.alpha_composite(fr, ov)

    # Logo (serve paste separato per RGBA img)
    paste_logo(fr, LOGO_C, W//2, 205, a=e(t, 0, 0.65))

    return to_rgb(fr)

# ─────────────────────────────────────────────────────────────────────────────
# SCENE 2 — Chi siamo (5s)
# Gradient bg · descrizione · valori
# ─────────────────────────────────────────────────────────────────────────────
def s2(t):
    fr = frame(GRAD_PIL)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d  = ImageDraw.Draw(ov)

    d.rectangle([(0, 0), (W, 6)], fill=GOLD + (255,))

    ov_text(d, "C H I   S I A M O", fb(44), NAVY, W//2, 155, e(t, 0, 0.45))
    bar_grow(d, 195, e(t, 0.25, 0.4), 170, GOLD)

    righe = [
        ("Boutique indipendente specializzata in",    0.35, 320),
        ("Mergers & Acquisitions, Capital Raising",   0.60, 430),
        ("e Advisory Strategico",                     0.85, 540),
    ]
    for testo, t0, y in righe:
        a = e(t, t0, 0.45)
        ov_text(d, testo, fl(58), NAVY, W//2, y, a, dy=int(26*(1-a)))

    bar_grow(d, 610, e(t, 1.15, 0.4), 480, GOLD)

    a5 = e(t, 1.3, 0.5)
    ov_text(d, "per le aziende mid-market italiane e internazionali",
            fl(42), MID, W//2, 710, a5, dy=int(18*(1-a5)))

    a6 = e(t, 1.9, 0.5)
    ov_text(d, "Indipendenza  ·  Eccellenza  ·  Riservatezza",
            fl(34), GOLD, W//2, 860, a6)

    d.rectangle([(0, H-6), (W, H)], fill=GOLD + (255,))
    fr = Image.alpha_composite(fr, ov)
    return to_rgb(fr)

# ─────────────────────────────────────────────────────────────────────────────
# SCENE 3 — Numeri (8s)
# Navy bg · "22+" conta · servizi
# ─────────────────────────────────────────────────────────────────────────────
def s3(t):
    fr = frame(DARK_PIL)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d  = ImageDraw.Draw(ov)

    d.rectangle([(0, 0), (W, 6)],     fill=GOLD + (255,))
    d.rectangle([(0, H-6), (W, H)],   fill=GOLD + (255,))

    ov_text(d, "T R A C K   R E C O R D", fl(38), GOLD, W//2, 140, e(t, 0, 0.4))
    bar_grow(d, 178, e(t, 0.25, 0.4), 280, GOLD)

    # numero che sale
    prog = e(t, 0.35, 2.3)
    num  = int(prog * 22)
    suf  = "+" if num >= 22 else ""
    a_n  = e(t, 0.35, 0.45)
    ov_text(d, f"{num}{suf}", fb(265), WHITE, W//2, 440, a_n, dy=int(45*(1-a_n)))

    a_sub = e(t, 1.4, 0.5)
    ov_text(d, "T R A N S A Z I O N I   A D V I S O R Y",
            fl(44), GOLD, W//2, 590, a_sub, dy=int(22*(1-a_sub)))

    bar_grow(d, 640, e(t, 1.9, 0.4), 460, DEEP)

    # 4 servizi in 2x2
    servizi = [
        ("M&A Advisory",       1.9,  W//4,     720),
        ("Debt Advisory",      2.2,  3*W//4,   720),
        ("Financial Advisory", 2.5,  W//4,     790),
        ("Private Placement",  2.8,  3*W//4,   790),
    ]
    for testo, t0, cx, cy in servizi:
        a = e(t, t0, 0.4)
        ov_text(d, testo, fl(38), (138, 170, 191), cx, cy, a, dy=int(14*(1-a)))

    a_yr = e(t, 3.4, 0.5)
    ov_text(d, "D A L   2 0 1 6   A L   2 0 2 5", fl(30), MID, W//2, 910, a_yr)

    fr = Image.alpha_composite(fr, ov)
    return to_rgb(fr)

# ─────────────────────────────────────────────────────────────────────────────
# SCENE 4 — Transazioni (10s)
# Navy bg · 2 colonne di deal appaiono in sequenza
# ─────────────────────────────────────────────────────────────────────────────
def s4(t):
    fr = frame(DARK_PIL)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d  = ImageDraw.Draw(ov)

    d.rectangle([(0, 0), (W, 6)],   fill=GOLD + (255,))
    d.rectangle([(0, H-6), (W, H)], fill=GOLD + (255,))

    ov_text(d, "O U R   A D V I S O R Y   T R A N S A C T I O N S",
            fl(38), GOLD, W//2, 72, e(t, 0, 0.4))
    bar_grow(d, 108, e(t, 0.25, 0.45), 520, GOLD)

    # divisore verticale che scende
    adiv = e(t, 0.3, 0.5)
    if adiv > 0:
        lh = int((H - 160) * adiv)
        d.line([(W//2, 125), (W//2, 125 + lh)], fill=DEEP + (180,), width=2)

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

    y0, dy_row = 142, 112

    for i, (anno, nome) in enumerate(deals_l):
        t0 = 0.45 + i * 0.28
        a  = e(t, t0, 0.35)
        y  = y0 + i * dy_row
        if a > 0:
            d.rounded_rectangle([(52, y), (138, y+40)], radius=4,
                                 fill=DEEP + (int(255*a),))
            d.text((95, y+20), anno, font=fb(24), fill=GOLD+(int(255*a),), anchor="mm")
            ov_text_l(d, nome, fl(34), WHITE, 152, y+20, a, dy=int(14*(1-a)))
            d.line([(52, y+56), (W//2-30, y+56)], fill=DEEP+(int(160*a),), width=1)

    for i, (anno, nome) in enumerate(deals_r):
        t0 = 0.6 + i * 0.28
        a  = e(t, t0, 0.35)
        y  = y0 + i * dy_row
        if a > 0:
            xb = W//2 + 32
            d.rounded_rectangle([(xb, y), (xb+86, y+40)], radius=4,
                                 fill=DEEP + (int(255*a),))
            d.text((xb+43, y+20), anno, font=fb(24), fill=GOLD+(int(255*a),), anchor="mm")
            ov_text_l(d, nome, fl(34), WHITE, W//2+132, y+20, a, dy=int(14*(1-a)))
            d.line([(xb, y+56), (W-52, y+56)], fill=DEEP+(int(160*a),), width=1)

    fr = Image.alpha_composite(fr, ov)
    return to_rgb(fr)

# ─────────────────────────────────────────────────────────────────────────────
# SCENE 5 — Team (8s)
# Gradient bg · nomi appaiono in scalata
# ─────────────────────────────────────────────────────────────────────────────
def s5(t):
    fr = frame(GRAD_PIL)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d  = ImageDraw.Draw(ov)

    d.rectangle([(0, 0), (W, 6)],   fill=GOLD + (255,))
    d.rectangle([(0, H-6), (W, H)], fill=GOLD + (255,))

    ov_text(d, "I L   N O S T R O   T E A M", fb(48), NAVY, W//2, 92, e(t, 0, 0.4))
    bar_grow(d, 134, e(t, 0.2, 0.4), 190, GOLD)

    # divisore verticale fisso
    d.line([(W//2, 148), (W//2, H-20)], fill=(184,200,216,160), width=2)

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

    col_w = W // 2
    row_h = (H - 185) // 5

    for i, (nome, ruolo) in enumerate(team):
        col = i % 2
        row = i // 2
        cx  = col * col_w + col_w // 2 + 20
        cy  = 168 + row * row_h + row_h // 2
        t0  = 0.3 + (row * 2 + col) * 0.18
        a   = e(t, t0, 0.38)
        ov_text(d, nome,  fb(34), NAVY, cx, cy - 20, a, dy=int(14*(1-a)))
        ov_text(d, ruolo, fl(26), GOLD, cx, cy + 18, a)

    fr = Image.alpha_composite(fr, ov)
    return to_rgb(fr)

# ─────────────────────────────────────────────────────────────────────────────
# SCENE 6 — Chiusura (8s)
# Navy bg · logo bianco · grazie · sito
# ─────────────────────────────────────────────────────────────────────────────
def s6(t):
    fr = frame(DARK_PIL)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d  = ImageDraw.Draw(ov)

    d.rectangle([(0, 0), (W, 6)],   fill=GOLD + (255,))
    d.rectangle([(0, H-6), (W, H)], fill=GOLD + (255,))

    bar_grow(d, 295, e(t, 0.55, 0.5), 420, GOLD)

    a1 = e(t, 0.7, 0.5)
    ov_text(d, "Grazie a tutti coloro che", fl(74), WHITE, W//2, 420, a1, dy=int(26*(1-a1)))

    a2 = e(t, 1.05, 0.5)
    ov_text(d, "hanno creduto in noi", fl(74), WHITE, W//2, 520, a2, dy=int(26*(1-a2)))

    bar_grow(d, 598, e(t, 1.45, 0.45), 420, GOLD)

    a3 = e(t, 1.65, 0.5)
    ov_text(d, "in questi 10 anni di avventura", fl(56), GOLD, W//2, 695, a3, dy=int(20*(1-a3)))

    a4 = e(t, 2.3, 0.55)
    ov_text(d, "a n t c a p i t a l . i t", fl(40), MID, W//2, 880, a4)

    fr = Image.alpha_composite(fr, ov)

    paste_logo(fr, LOGO_W, W//2, 200, a=e(t, 0, 0.6))

    return to_rgb(fr)

# ─────────────────────────────────────────────────────────────────────────────
# Assembla
# ─────────────────────────────────────────────────────────────────────────────
def mk(fn, dur, fi=0.2, fo=0.2):
    clip = VideoClip(fn, duration=dur)
    return clip.with_effects([FadeIn(fi), FadeOut(fo)])

def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    print("Generazione video v2...")

    clips = [
        mk(s1, 8),
        mk(s2, 5),
        mk(s3, 8),
        mk(s4, 10),
        mk(s5, 8),
        mk(s6, 8),
    ]

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(
        OUT, fps=FPS, codec="libx264", audio=False,
        preset="medium", bitrate="8000k", logger="bar"
    )
    print(f"\nPronto: {OUT}")

if __name__ == "__main__":
    main()
