#!/usr/bin/env python3
"""Generate the favicons and the Open Graph link-preview card.

    python3 tools/make-images.py

Rendered with headless Chrome so the typography matches the site, then downscaled
with Pillow (sharper than asking Chrome to render 32 px text). Re-run after changing
the avatar or the palette in assets/css/site.css.

Outputs: favicon.svg, favicon-32.png, apple-touch-icon.png, images/og-card.jpg
"""

import pathlib
import re
import subprocess
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SANS = ('-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", '
        "Arial, sans-serif")


def token(name, default):
    """Read a custom property out of the light palette in site.css."""
    css = (ROOT / "assets/css/site.css").read_text()
    root = re.search(r":root \{(.*?)\n\}", css, re.S).group(1)
    m = re.search(rf"--{name}:\s*([^;]+);", root)
    return m.group(1).strip() if m else default


def shoot(html, width, height, out):
    tmp = ROOT / "_render.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         f"--window-size={width},{height}", f"--screenshot={out}", f"file://{tmp}"],
        capture_output=True,
    )
    tmp.unlink()
    if not pathlib.Path(out).exists():
        sys.exit(f"Chrome produced no output for {out}")


def main():
    teal = token("sidebar-bg", "#1d7a63")
    fg = token("sidebar-fg", "#ffffff")

    # --- favicon.svg: a JL monogram, legible down to 16 px ------------------------
    (ROOT / "favicon.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
        f'  <rect width="64" height="64" rx="13" fill="{teal}"/>\n'
        f'  <text x="32" y="45" text-anchor="middle" font-family="{SANS}"\n'
        f'        font-size="35" font-weight="700" fill="{fg}">JL</text>\n'
        f"</svg>\n",
        encoding="utf-8",
    )

    # --- favicon PNGs: render large, downscale ------------------------------------
    icon_html = f"""<style>
      html,body{{margin:0;width:180px;height:180px}}
      .i{{width:180px;height:180px;background:{teal};border-radius:37px;
          display:flex;align-items:center;justify-content:center}}
      span{{font:700 98px {SANS};color:{fg};letter-spacing:-2px}}
    </style><div class="i"><span>JL</span></div>"""
    big = ROOT / "apple-touch-icon.png"
    shoot(icon_html, 180, 180, big)
    Image.open(big).resize((32, 32), Image.LANCZOS).save(ROOT / "favicon-32.png")

    # --- Open Graph card, 1200x630 ------------------------------------------------
    # Text must survive being shown ~360 px wide in a Slack unfurl, hence the scale.
    card_html = f"""<style>
      html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
      body{{background:{teal};color:{fg};font-family:{SANS};
            display:flex;align-items:center;gap:62px;padding:0 78px;box-sizing:border-box}}
      .pic{{flex:none;width:264px;height:264px;border-radius:50%;overflow:hidden;
            box-shadow:0 10px 40px rgba(0,0,0,.28)}}
      .pic img{{width:100%;height:100%;object-fit:cover;display:block}}
      h1{{margin:0 0 18px;font-size:78px;font-weight:700;letter-spacing:-2px;line-height:1}}
      p{{margin:0;font-size:30px;line-height:1.45;opacity:.93}}
      .aff{{margin-top:20px;font-size:27px;opacity:.78}}
    </style>
    <div class="pic"><img src="images/avatar.jpg"></div>
    <div>
      <h1>Joel Leja</h1>
      <p>Associate Professor of Astronomy &amp; Astrophysics<br>
         Dr. Keiko Miwa Ross Mid-Career Professor</p>
      <p class="aff">The Pennsylvania State University</p>
    </div>"""
    png = ROOT / "_og.png"
    shoot(card_html, 1200, 630, png)
    Image.open(png).convert("RGB").save(
        ROOT / "images/og-card.jpg", "JPEG", quality=88, optimize=True, progressive=True
    )
    png.unlink()

    for f in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png",
              "images/og-card.jpg"):
        p = ROOT / f
        size = f" {Image.open(p).size}" if not f.endswith(".svg") else ""
        print(f"  {f:<26} {p.stat().st_size / 1024:6.1f} KB{size}")


if __name__ == "__main__":
    main()
