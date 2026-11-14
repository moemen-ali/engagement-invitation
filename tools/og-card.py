"""Renders the link-preview card (WhatsApp / social) from the site's own content and art.

    python tools/og-card.py [og-card.jpg]

1200x630: the stage photo in the venue-arch frame on the left; rings, names (English + Arabic), date and venue on
the right, on the site's lavender. Names, date and venue are read from CONFIG in index.html, the rings SVG and the
--venue-arch mask from the page itself, so re-run this after changing any of them.
Requires Playwright with Edge/Chrome (or `playwright install chromium`) and internet for Google Fonts.
"""
import pathlib
import re
import sys
from datetime import datetime

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "og-card.jpg")
page = (ROOT / "index.html").read_text(encoding="utf-8")


def cfg(key):
    return re.search(rf'{key}: "([^"]*)"', page).group(1)


start = datetime.fromisoformat(cfg("start"))      # keeps the +02:00 offset, i.e. Cairo time
date_line = f"{start:%A} · {start.day} {start:%B %Y} · {start.hour % 12 or 12}:{start:%M} {'PM' if start.hour >= 12 else 'AM'}"
rings = re.search(r'<svg class="rings".*?</svg>', page, re.S).group(0)
mask = re.search(r"--venue-arch: (url\(.*?\));", page, re.S).group(1)
symbol = re.search(r'<symbol id="venueArch".*?</symbol>', page, re.S).group(0)

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Amiri&family=Cormorant+Garamond:ital@0;1&family=Great+Vibes&family=Jost:wght@400;500&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; box-sizing: border-box }}
  body {{ width: 1200px; height: 630px; overflow: hidden; display: flex; align-items: center; gap: 64px; padding: 0 70px 0 92px;
         background: linear-gradient(135deg, #ece8fc 0%, #e4e6fb 55%, #dbe3fa 100%); font-family: Jost, sans-serif; color: #2e2766 }}
  .frame {{ position: relative; flex: none; width: 390px; height: 520px; filter: drop-shadow(0 22px 26px rgba(46,39,102,.22)) }}
  .shape {{ position: absolute; inset: 0; background: #fff; padding: 10px; -webkit-mask: {mask} center/100% 100% no-repeat }}
  .shape img {{ width: 100%; height: 100%; object-fit: cover; -webkit-mask: {mask} center/100% 100% no-repeat }}
  .line {{ position: absolute; inset: -11px; width: calc(100% + 22px); height: calc(100% + 22px); overflow: visible;
          fill: none; stroke: #cfc6f3; stroke-width: 1.5 }}
  .text {{ flex: 1; text-align: center }}
  .rings {{ width: 132px; height: auto; display: block; margin: 0 auto 6px }}
  .eyebrow {{ font-weight: 500; font-size: 17px; letter-spacing: .32em; text-transform: uppercase; color: #6a4cc4 }}
  h1 {{ font: 400 104px/1.05 'Great Vibes', cursive; margin: 6px 0 0; white-space: nowrap }}
  h1 span {{ font: italic 400 52px 'Cormorant Garamond', serif; color: #6a4cc4; padding: 0 .32em }}
  .ar {{ font: 34px Amiri, serif; direction: rtl; margin-top: 2px }}
  .rule {{ width: 120px; height: 1px; background: #6a4cc4; opacity: .4; margin: 18px auto }}
  .date {{ font: italic 400 33px 'Cormorant Garamond', serif }}
  .venue {{ margin-top: 10px; font-size: 18px; letter-spacing: .2em; text-transform: uppercase; color: #585482 }}
</style></head><body>
<svg width="0" height="0" style="position:absolute"><defs>{symbol}</defs></svg>
<div class="frame">
  <svg class="line"><use href="#venueArch" width="100%" height="100%"/></svg>
  <div class="shape"><img src="{(ROOT / 'stage.jpg').as_uri()}"></div>
</div>
<div class="text">
  {rings}
  <p class="eyebrow">Engagement Celebration</p>
  <h1>{cfg("name1")}<span>&amp;</span>{cfg("name2")}</h1>
  <p class="ar">{cfg("name1Ar")} و {cfg("name2Ar")}</p>
  <div class="rule"></div>
  <p class="date">{date_line}</p>
  <p class="venue">{cfg("venue")} · {cfg("address")}</p>
</div>
</body></html>"""

tmp = ROOT / "og-card.tmp.html"
tmp.write_text(html, encoding="utf-8")
try:
    with sync_playwright() as p:
        for channel in ("msedge", "chrome", None):
            try:
                browser = p.chromium.launch(channel=channel) if channel else p.chromium.launch()
                break
            except Exception:
                continue
        pg = browser.new_page(viewport={"width": 1200, "height": 630})
        pg.goto(tmp.as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(OUT), type="jpeg", quality=86)
        browser.close()
finally:
    tmp.unlink(missing_ok=True)
print(OUT.name, OUT.stat().st_size // 1024, "KB")
