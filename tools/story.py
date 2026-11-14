"""Renders a 1080x1920 Instagram Story that looks like the site's hero section.

    python tools/story.py [story.jpg]

Lavender sky, string lights, sun glow, rings, names (English + Arabic), invite lines, date/time and venue, and the
SVG stage scene with roses and sea - all taken from index.html (CONFIG, rings, lights, scene), so re-run this after
changing any of them. Text stays out of Instagram's covered areas (top ~250px: profile bar; bottom ~260px: reply bar).
Leave the link sticker on the sea band. No couple illustration, by request.
Requires Playwright with Edge/Chrome (or `playwright install chromium`) and internet for Google Fonts.
"""
import pathlib
import re
import sys
from datetime import datetime

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "story.jpg")
page = (ROOT / "index.html").read_text(encoding="utf-8")


def cfg(key):
    return re.search(rf'{key}: "([^"]*)"', page).group(1)


def block(pattern):
    return re.search(pattern, page, re.S).group(0)


start = datetime.fromisoformat(cfg("start"))      # keeps the +02:00 offset, i.e. Cairo time
date_line = f"{start:%A} · {start.day} {start:%B %Y} · {start.hour % 12 or 12}:{start:%M} {'PM' if start.hour >= 12 else 'AM'}"
rings = block(r'<svg class="rings".*?</svg>')
lights = block(r'<svg class="lights".*?</svg>')
scene = block(r'<svg class="scene".*?</svg>')
invite_ar = re.search(r'<p class="ar invite-ar">(.*?)</p>', page).group(1)

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Amiri&family=Cormorant+Garamond:ital@0;1&family=Italianno&family=Jost:wght@400;500&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; box-sizing: border-box }}
  body {{ width: 1080px; height: 1920px; overflow: hidden; position: relative; font-family: Jost, sans-serif; color: #2e2766;
         text-align: center; background: linear-gradient(180deg, #e7e1fb 0%, #e8e8fc 34%, #dfe5fa 66%, #f8f7fe 100%) }}
  .lights {{ position: absolute; top: 0; left: 0; width: 100%; height: 99px }}  /* 1200x110 viewBox at 0.9 scale: round bulbs */
  .sun {{ position: absolute; top: 120px; right: 70px; width: 250px; height: 250px; border-radius: 50%; filter: blur(3px);
         background: radial-gradient(circle, rgba(243,217,164,.95) 0%, rgba(243,217,164,.4) 42%, rgba(243,217,164,0) 70%) }}
  .intro {{ position: absolute; top: 290px; left: 0; right: 0; padding: 0 60px }}
  .rings {{ width: 230px; height: auto; display: block; margin: 0 auto 26px }}
  .eyebrow {{ font-weight: 500; font-size: 25px; letter-spacing: .34em; text-transform: uppercase; color: #6a4cc4 }}
  h1 {{ font: 400 178px/1 'Italianno', cursive; margin-top: 18px; white-space: nowrap }}
  h1 span {{ font: italic 400 86px 'Cormorant Garamond', serif; color: #6a4cc4; padding: 0 .3em }}
  .ar {{ font-family: Amiri, serif; direction: rtl }}
  .names-ar {{ font-size: 62px; line-height: 1.4; margin-top: 6px }}
  .invite-ar {{ font-size: 40px; color: #585482; margin-top: 4px }}
  .tag {{ margin-top: 30px; font-size: 24px; letter-spacing: .28em; text-transform: uppercase; color: #585482 }}
  .rule {{ width: 160px; height: 1px; background: #6a4cc4; opacity: .4; margin: 34px auto }}
  .date {{ font: italic 400 54px 'Cormorant Garamond', serif }}
  .venue {{ margin-top: 16px; font-size: 26px; letter-spacing: .22em; text-transform: uppercase; color: #585482 }}
  .scene-wrap {{ position: absolute; left: 0; right: 0; bottom: 70px; height: 756px }}
  .scene {{ width: 100%; height: 100% }}
</style></head><body>
{lights}
<div class="sun"></div>
<div class="intro">
  {rings}
  <p class="eyebrow">Together with their families</p>
  <h1>{cfg("name1")}<span>&amp;</span>{cfg("name2")}</h1>
  <p class="ar names-ar">{cfg("name1Ar")} و {cfg("name2Ar")}</p>
  <p class="ar invite-ar">{invite_ar}</p>
  <p class="tag">Invite you to a seaside engagement celebration</p>
  <div class="rule"></div>
  <p class="date">{date_line}</p>
  <p class="venue">{cfg("venue")} · {cfg("address")}</p>
</div>
<div class="scene-wrap">{scene}</div>
</body></html>"""

tmp = ROOT / "story.tmp.html"
tmp.write_text(html, encoding="utf-8")
try:
    with sync_playwright() as p:
        for channel in ("msedge", "chrome", None):
            try:
                browser = p.chromium.launch(channel=channel) if channel else p.chromium.launch()
                break
            except Exception:
                continue
        pg = browser.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(tmp.as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        # report where the text block ends, to keep it clear of the stage art and Instagram's bars
        box = pg.evaluate("(() => { const r = document.querySelector('.intro').getBoundingClientRect(); return [Math.round(r.top), Math.round(r.bottom)] })()")
        arch_top = pg.evaluate("Math.round(document.querySelector('.scene-wrap').getBoundingClientRect().top + 756 * 74 / 700)")
        pg.screenshot(path=str(OUT), type="jpeg", quality=90)
        browser.close()
finally:
    tmp.unlink(missing_ok=True)
print(OUT.name, f"{OUT.stat().st_size // 1024} KB | text block y {box[0]}-{box[1]} | arches start ~y {arch_top}")
