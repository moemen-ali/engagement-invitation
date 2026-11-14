"""Automated pre-merge checks for the invitation page.

Usage:
    python -m http.server 8000            # serve the repo root in another terminal
    python tools/check.py http://localhost:8000/

Needs `pip install playwright` and an installed Edge or Chrome (or `playwright install chromium`).
Exits non-zero if any check fails.
"""
import sys
from urllib.parse import unquote

from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/"
WIDTHS = [(375, 812), (768, 1024), (1280, 800)]
failures = []


def check(ok, label):
    print(("  ok    " if ok else "  FAIL  ") + label)
    if not ok:
        failures.append(label)


def launch(p):
    for channel in ("msedge", "chrome", None):
        try:
            return p.chromium.launch(channel=channel) if channel else p.chromium.launch()
        except Exception:
            continue
    sys.exit("No browser found: install Edge/Chrome or run `playwright install chromium`.")


with sync_playwright() as p:
    browser = launch(p)
    for w, h in WIDTHS:
        print(f"{w}px")
        page = browser.new_page(viewport={"width": w, "height": h})
        errors = []
        page.on("console", lambda m: m.type == "error" and errors.append(m.text))
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(URL, wait_until="networkidle")

        check(not errors, f"no console errors {errors or ''}")
        s1 = page.inner_text("#s"); page.wait_for_timeout(1500); s2 = page.inner_text("#s")
        check(s1 != s2, f"countdown ticking ({s1} -> {s2})")
        check(page.evaluate("document.documentElement.scrollWidth - innerWidth") <= 0, "no horizontal scrolling")
        page.evaluate("document.querySelector('[data-stage]').scrollIntoView()")
        page.wait_for_function("document.querySelector('[data-stage]').complete")
        check(page.evaluate("document.querySelector('[data-stage]').naturalWidth > 0"), "stage image loads")
        small = page.evaluate("""[...document.querySelectorAll('a,button,input:not([type=radio]),select,textarea,.choice label')]
            .map(e => [e.textContent.trim().slice(0, 30) || e.id, Math.round(e.getBoundingClientRect().height)])
            .filter(([, h]) => h && h < 44)""")
        check(not small, f"tap targets >= 44px {small or ''}")
        check(page.get_attribute("[data-maps]", "href").startswith("https://"), "Maps link set")
        check("calendar.google.com" in page.get_attribute("[data-calendar]", "href"), "calendar link set")
        page.close()

    print("RSVP flow (375px)")
    page = browser.new_page(viewport={"width": 375, "height": 812})
    page.goto(URL, wait_until="networkidle")
    page.evaluate("window.open = u => { window.__opened = u }")
    page.click("button[type=submit]")
    check(page.is_visible("#f-name-err") and not page.evaluate("window.__opened || null"), "empty name shows error, no WhatsApp")
    page.fill("#f-name", "Test Guest"); page.select_option("#f-guests", "2"); page.fill("#f-msg", "Mabrook!")
    page.click("button[type=submit]")
    opened = page.evaluate("window.__opened || ''")
    check(opened.startswith("https://wa.me/"), "opens wa.me link")
    if "text=" in opened:
        print("\n".join("        " + line for line in unquote(opened.split("text=")[1]).splitlines()))
    browser.close()

print("\nAll checks passed." if not failures else f"\n{len(failures)} check(s) failed.")
sys.exit(1 if failures else 0)
