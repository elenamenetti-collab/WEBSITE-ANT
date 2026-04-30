#!/usr/bin/env python3
"""
Registra antcapital-10anni-v3.html come MP4
Usa Playwright per aprire il browser headless e registrare l'animazione,
poi moviepy per convertire webm → mp4.
"""

import subprocess, sys, os, time, shutil
from pathlib import Path

# ── Dipendenze ────────────────────────────────────────────────────────────────
def pip(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Installazione Playwright...")
    pip("playwright")
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    from playwright.sync_api import sync_playwright

try:
    from moviepy import VideoFileClip
except ImportError:
    print("Installazione moviepy...")
    pip("moviepy")
    from moviepy import VideoFileClip

# ── Configurazione ────────────────────────────────────────────────────────────
SRC_HTML   = Path("G:/Drive condivisi/Server CF/2.1 Ideas/0. Pjt Interno/10 years/antcapital-10anni-v3.html")
SRC_ASSETS = Path("G:/Drive condivisi/Server CF/2.1 Ideas/0. Pjt Interno/4. Website/WEBSITE-ANT")
LOCAL      = Path(r"C:\tmp\ant_video")
OUT        = Path("G:/Drive condivisi/Server CF/2.1 Ideas/0. Pjt Interno/Video/antcapital-10anni-v3.mp4")
TMP        = Path(r"C:\tmp\_webm")

W, H     = 1600, 900   # 16:9
DURATION = 20          # secondi (animazione ~16s + 4s buffer)

# ── Copia assets in locale (Playwright non accede ai drive virtuali) ───────────
if LOCAL.exists():
    shutil.rmtree(LOCAL)
LOCAL.mkdir(parents=True)
TMP.mkdir(parents=True, exist_ok=True)
OUT.parent.mkdir(parents=True, exist_ok=True)

shutil.copy2(SRC_HTML, LOCAL / "antcapital-10anni-v3.html")
for folder in ["images", "Loghi"]:
    src_f = SRC_ASSETS / folder
    if src_f.exists():
        shutil.copytree(src_f, LOCAL / folder)
        print(f"  {folder}/  ({len(list((LOCAL/folder).rglob('*')))} file)")

HTML = LOCAL / "antcapital-10anni-v3.html"

print(f"\nFile:        {HTML}")
print(f"Output:      {OUT}")
print(f"Risoluzione: {W}×{H}")
print(f"Durata:      {DURATION}s\n")

# ── Registrazione ─────────────────────────────────────────────────────────────
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-web-security"])
    ctx = browser.new_context(
        viewport={"width": W, "height": H},
        record_video_dir=str(TMP),
        record_video_size={"width": W, "height": H},
        device_scale_factor=1,
    )
    page = ctx.new_page()
    page.goto(HTML.as_uri())
    page.wait_for_load_state("networkidle")
    time.sleep(0.5)  # attendi font Google

    # Adatta il frame a pieno schermo, nascondi controlli
    page.evaluate("""() => {
        const f = document.querySelector('.F');
        f.style.cssText = 'width:100vw;height:100vh;border-radius:0;';
        document.body.style.cssText =
            'margin:0;padding:0;overflow:hidden;background:#000;' +
            'display:block;align-items:unset;justify-content:unset;';
        document.querySelector('.cb').style.display    = 'none';
        document.querySelector('.strip').style.display = 'none';
    }""")
    time.sleep(0.2)

    # Riavvia l'animazione dall'inizio
    page.evaluate("rs(); setTimeout(tp, 150)")

    print(f"Registrazione in corso ({DURATION}s)...")
    time.sleep(DURATION)

    ctx.close()
    browser.close()

# ── Conversione webm → mp4 ────────────────────────────────────────────────────
webm_files = list(TMP.glob("*.webm"))
if not webm_files:
    print("ERRORE: nessun file .webm trovato nella cartella temporanea")
    sys.exit(1)

webm = webm_files[0]
print(f"\nConversione {webm.name} → MP4...")

clip = VideoFileClip(str(webm))
clip.write_videofile(
    str(OUT),
    codec="libx264",
    audio=False,
    fps=30,
    preset="medium",
    bitrate="8000k",
    logger="bar",
)
clip.close()

shutil.rmtree(TMP)
shutil.rmtree(LOCAL)
print(f"\nVideo pronto: {OUT}")
