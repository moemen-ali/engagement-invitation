# Mo'men & Alaa — Engagement Invitation Website

A single-page, mobile-first invitation website for **Mo'men & Alaa's** open-air engagement party by the sea.
Guests open the link (mostly from WhatsApp on a phone), see the date, venue and dress code, and RSVP through WhatsApp.

- **Stack:** one static `index.html` (HTML + CSS + vanilla JS). No framework, no build step, no npm, no backend.
- **Live site:** _not deployed yet — add the URL here once it is._

> **Keep this file current.** Any change to the site's content, behaviour, design, files or decisions must update the
> relevant section below **and** add an entry to the [Changelog](#changelog), in the same commit.

---

## Contents

1. [The event at a glance](#the-event-at-a-glance)
2. [Before launch: open items](#before-launch-open-items)
3. [Quick start](#quick-start)
4. [Repository layout](#repository-layout)
5. [How the page works](#how-the-page-works)
6. [Editing guide (common tasks)](#editing-guide-common-tasks)
7. [Page sections](#page-sections)
8. [Design system](#design-system)
9. [Hero stage art (SVG generator)](#hero-stage-art-svg-generator)
10. [Images](#images)
11. [Design skill (ui-ux-pro-max)](#design-skill-ui-ux-pro-max)
12. [Checks before merging](#checks-before-merging)
13. [Deployment](#deployment)
14. [Collaboration workflow](#collaboration-workflow)
15. [Decision log](#decision-log)
16. [Changelog](#changelog)
17. [Credits and licences](#credits-and-licences)

---

## The event at a glance

| | |
|---|---|
| Couple | Mo'men & Alaa — مؤمن و آلاء |
| Date | Saturday 21 November 2026 |
| Time | 3:00 PM – 7:00 PM, Cairo time (UTC+02:00) |
| Venue | The Blue View, Engineers Club, Alexandria |
| Map | <https://maps.app.goo.gl/6usG7rS5s6MGmmM66> (pin at 31.2392, 29.9532 on the Corniche) |
| Setting | Open air, on grass, white sculpted arches with flowers, sea behind the stage |
| RSVP deadline | 18 November |
| RSVP channel | WhatsApp message to the number in `CONFIG.whatsapp` |

All of these values live in one place: the `CONFIG` object at the bottom of `index.html` (see [Editing guide](#editing-guide-common-tasks)).

## Before launch: open items

These must be done before the link is sent to guests:

- [ ] **WhatsApp number.** `CONFIG.whatsapp` is still the placeholder `201000000000`, so RSVPs go nowhere.
      Format: country code + number, no `+`, no spaces, no leading zero (e.g. `2010XXXXXXXX`).
- [ ] **Link-preview image URL.** After deploying, change `<meta property="og:image" content="og-image.jpg">`
      to the full URL (e.g. `https://<site>/og-image.jpg`). WhatsApp ignores relative image URLs.
- [ ] **Arabic spelling of Alaa.** The site uses **آلاء** (the standard spelling). If the family writes it الاء,
      change `CONFIG.name2Ar`.
- [ ] **End time.** 7:00 PM was assumed (no end time was given). Change `CONFIG.end` if needed.
- [ ] Add the live URL at the top of this file.

## Quick start

```bash
git clone <repo-url>
cd <repo>
python -m http.server 8000      # or: python3 -m http.server 8000
# open http://localhost:8000
```

Open it at phone width first (browser dev tools → 375px), because that is how most guests will see it.
Opening `index.html` directly from disk also works, but a local server matches production more closely.

## Repository layout

```
.
├── index.html                    ← the whole site: markup, CSS, JS, inline SVG art
├── stage.jpg                     ← venue stage art shown in the "Under the Arches" frame (900×1200, ~180 KB)
├── og-image.jpg                  ← landscape crop of the stage art for link previews (1200×630, ~105 KB)
├── stage.png                     ← original source art (1086×1448, 2.6 MB). Not used by the page
├── tools/
│   ├── stage-art.py              ← generates the hero's inline SVG stage scene + arch line-drawing symbol
│   └── check.py                  ← automated browser checks (see "Checks before merging")
├── .claude/skills/ui-ux-pro-max/ ← design-intelligence skill for Claude Code (MIT)
├── CLAUDE.md                     ← rules for Claude Code (AI assistant) working in this repo
├── README.md                     ← this file: full project context for collaborators
└── .gitignore
```

Only `index.html`, `stage.jpg` and `og-image.jpg` are needed by the live site. The only external dependency is Google Fonts.

## How the page works

### Content binding

`index.html` contains **no hard-coded event details** in the markup. Elements carry empty `data-*` attributes and a
small script fills them from `CONFIG` on load:

| Attribute | Filled with |
|---|---|
| `data-name1`, `data-name2` | English names |
| `data-names-ar` | `"<name1Ar> و <name2Ar>"` |
| `data-when` | `Saturday · 21 November 2026 · 3:00 PM` |
| `data-weekday`, `data-date-long` | `Saturday`, `21 November 2026` |
| `data-time`, `data-until` | `3:00 PM`, `Until 7:00 PM` |
| `data-venue`, `data-address` | venue name, address |
| `data-rsvp-by` | RSVP deadline text |
| `data-date-dots` | `21 · 11 · 2026` (footer) |
| `data-stage` | `src` of the stage image |
| `data-maps` | `href` of "Open in Maps" |
| `data-calendar` | `href` of "Add to calendar" (Google Calendar template link) |
| `data-count-label` | countdown heading (becomes "Today's the day" at zero) |

**Exception:** `<title>`, `<meta name="description">` and the `og:*` tags in `<head>` repeat the names, date and
venue as plain text, because WhatsApp's link preview does not run JavaScript. Update them by hand whenever `CONFIG` changes.

### Time zone

Times are ISO strings with the `+02:00` offset (`2026-11-21T15:00:00+02:00`), and every date/time is formatted
with `timeZone: 'Africa/Cairo'`. Guests abroad still see Cairo time. Keep it that way.

### Behaviour

- **Countdown:** ticks every second to `CONFIG.start`; at zero it shows `00` and the heading changes to "Today's the day".
  It uses `role="timer"` with `aria-live="off"` so screen readers aren't spammed every second.
- **Add to calendar:** Google Calendar link with title, UTC start/end, location and the Maps link in the details.
- **RSVP:** no backend. On submit, the form builds a message and opens `https://wa.me/<number>?text=…`:
  ```
  RSVP — Mo'men & Alaa's engagement
  Name: <name>
  Joyfully yes ✨ | Sadly no
  Guests: <1–4>
  Note: <optional note>
  ```
  If the name is empty, an inline error appears under the field and focus moves there; it clears as you type.
- **Scroll reveal:** sections fade/slide in once (`.reveal` → `.in` via `IntersectionObserver`). The `js` class on
  `<html>` gates this, so content stays visible if JavaScript fails.
- **Reduced motion:** with `prefers-reduced-motion: reduce`, reveal, sea swell, bulb glow, button motion and smooth
  scrolling are all switched off.

## Editing guide (common tasks)

All in the `CONFIG` object near the bottom of `index.html`:

```js
const CONFIG = {
    name1: "Mo'men",
    name2: "Alaa",
    name1Ar: "مؤمن",
    name2Ar: "آلاء",
    start: "2026-11-21T15:00:00+02:00",   // Saturday 21 Nov 2026, 3:00 PM Cairo time
    end: "2026-11-21T19:00:00+02:00",
    venue: "The Blue View",
    address: "Engineers Club, Alexandria",
    mapsUrl: "https://maps.app.goo.gl/6usG7rS5s6MGmmM66",
    stageImage: "stage.jpg",
    whatsapp: "201000000000",             // TODO: real number
    rsvpBy: "18 November"
};
```

| Task | What to change |
|---|---|
| Set the RSVP WhatsApp number | `whatsapp` (country code + number, no `+`/spaces/leading zero) |
| Change date or time | `start` / `end` (keep `+02:00`), then the `<head>` meta text, then the event table in this README |
| Change venue or map | `venue`, `address`, `mapsUrl`, then the `<head>` meta text |
| Change names | `name1`, `name2`, `name1Ar`, `name2Ar`, then `<title>`, `og:title`, `description`, footer is automatic |
| Change RSVP deadline | `rsvpBy` (must be **before** the event date) |
| Replace the stage photo | see [Images](#images); update `stageImage` and the `.arch` `aspect-ratio` if the ratio changes |
| Change guest-count options | the `<select id="f-guests">` options in the RSVP form |
| Change dress-code tips | the `.pills` list in the Dress code section (keep the SVG icon + text pattern) |

## Page sections

In order:

1. **Hero** — lavender sky gradient, soft sun glow (top right), festoon string lights with glowing bulbs; eyebrow
   "Together with their families"; names in Great Vibes script with a Cormorant `&`; Arabic names (Amiri); Arabic invite
   line «بكل الحب ندعوكم لمشاركتنا فرحة خطوبتنا»; "Invite you to a seaside engagement celebration"; date line;
   **Kindly RSVP** button (jumps to `#rsvp`); then the **SVG stage scene** (see [Hero stage art](#hero-stage-art-svg-generator)).
2. **Countdown** — four arch-topped tiles: Days, Hours, Mins, Secs.
3. **Under the Arches** — short venue paragraph + `stage.jpg` in an arch frame (white border, lilac outline ring).
   Two columns from 860px wide (text left, photo right), stacked on phones.
4. **The Details** — three arch-topped cards with SVG icons: When / Time / Where (+ "Open in Maps"), then an
   **Add to calendar** button.
5. **Coastal Chic** (dress code) — five labelled arch swatches (Pearl, Lilac, Periwinkle, Sea blue, Indigo) and three
   tip pills with icons: sunglasses welcome; flats or block heels (it's on grass); a light layer for the sea breeze.
6. **Will You Join Us?** (RSVP, `id="rsvp"`) — name, attending (Joyfully yes / Sadly no), number of guests (1–4),
   optional note, **Send RSVP via WhatsApp**. A faint line drawing of the central arch sits behind the form.
7. **Footer** — names in script, Arabic names, «في انتظاركم», date as `21 · 11 · 2026`, faint arch line drawing.

"Our Story" and "Morning Plan" (timeline) sections were **intentionally removed** — do not add them back.

## Design system

**Direction:** "refined coastal" in **purple and blue shades** (chosen by the couple): airy, bright afternoon,
romantic. Lavender sky, periwinkle and violet roses, sea-blue water, white sculptural arches. The stage photo keeps
its natural colours; everything else uses these tokens (CSS custom properties in `:root`):

| Token | Value | Use |
|---|---|---|
| `--violet` | `#6a4cc4` | primary accent, buttons, eyebrow labels, links |
| `--indigo` | `#2e2766` | headings, names, button hover |
| `--blue` | `#3a64c8` | sea, swatch |
| `--peri` | `#9aaaf2` | periwinkle accents, roses |
| `--lilac` | `#d9d2f7` | borders, line art |
| `--mist` | `#efedfc` | alternate section background |
| `--pearl` | `#f8f7fe` | main background |
| `--glow` | `#f3d9a4` | sun glow and bulbs only (sparingly) |
| `--ink` | `#262249` | body text |
| `--soft` | `#585482` | secondary text |

**Contrast (WCAG):** every text/background pair in use is ≥ 4.5:1 — e.g. ink on pearl 14.0, soft on pearl 6.6,
violet on white 6.1, white on violet 6.1, soft on lilac 4.8 (tightest). Re-check if you change a token.

**Typography**

| Role | Font | Notes |
|---|---|---|
| Couple's names | Great Vibes | script; only for names (hero h1, footer) |
| Headings | Cormorant Garamond 400 | italic for accents (`&`, date line, captions) |
| Body | Jost 300, 1rem, line-height 1.7 | |
| Labels / eyebrows | Jost 500, uppercase, letter-spacing .2–.35em | never smaller than .75rem |
| Arabic | Amiri | `.ar` class with `direction: rtl` |

**Motifs:** arches (rounded tops — countdown tiles, cards, swatches, photo frame, favicon) and soft waves.
Reuse these rather than inventing new shapes.

**Icons:** inline stroke SVGs (`.icon`: 24px grid, 1.6 stroke, round caps), `aria-hidden="true"`, next to visible text.
No emoji as icons.

**Interaction & accessibility**

- Buttons, inputs, choices and links are ≥ 44px tall; form text is 1rem so iOS Safari doesn't zoom on focus.
- Visible focus: 2px indigo outline on links/buttons, violet ring on inputs, outline on the focused radio choice.
- Every form field has a `<label>`; the attending choice is a `<fieldset>` labelled by its heading; radios are
  visually hidden but keyboard-accessible.
- Images have `alt`; decorative SVGs are `aria-hidden`; swatches have visible names (not colour-only).

**Motion:** gentle only — scroll reveal (0.7s), sea swell drift (10s), bulb glow (3.2s). All off under reduced motion.

**Don't:** dark/night themes, sunset orange as a main colour, pink or red accents (keep roses on the blue side of lavender).

## Hero stage art (SVG generator)

The hero's stage scene is inline SVG modelled on the real venue stage: a **wavy central arch** with a raised relief line,
two plain **side arches**, ~100 **roses/blooms** with sage leaves cascading down the arches (lavender `#b7a6ee`, violet
`#8a70dc`, periwinkle `#9aaaf2`, blue `#6f8fe0`, pale lilac, white), a blue **sea band** with drifting white swell lines
that fades into the page, and a white **stage platform** with steps.

It is produced by [`tools/stage-art.py`](tools/stage-art.py) (seeded random, so the output is stable):

```bash
python tools/stage-art.py out/          # writes out/scene.svg, out/archline.svg, out/preview.html
```

Then replace in `index.html`:
- the `<svg class="scene" …>…</svg>` block with `scene.svg`;
- the `<symbol id="archLine" …>…</symbol>` (inside the hidden sprite at the top of `<body>`) with `archline.svg`
  — this is the faint arch line drawing used behind the RSVP form and footer.

`preview.html` lets you look at the art on its own first. Layout rules:
- Phones (≤ 640px): the scene sits in a square box with `preserveAspectRatio="xMidYMax slice"`, so it crops to the central arch.
- Wider screens: height `min(56svh, 620px)` at the full 1000×700 ratio, showing all three arches.
- The SVG has `overflow="visible"` so the sea band runs the full viewport width (the hero clips it).

## Images

| File | Size | Use |
|---|---|---|
| `stage.png` | 1086×1448, 2.6 MB | original source art — keep it, edit/export from it |
| `stage.jpg` | 900×1200, ~180 KB, JPEG q80 progressive | stage section photo (must stay ≤ 400 KB) |
| `og-image.jpg` | 1200×630, ~105 KB | WhatsApp / social link preview (arches + sea crop) |

To regenerate both from the source (requires Pillow):

```python
from PIL import Image
im = Image.open('stage.png').convert('RGB')
im.resize((900, 1200), Image.LANCZOS).save('stage.jpg', 'JPEG', quality=80, optimize=True, progressive=True)
im.crop((0, 470, 1086, 470 + round(1086 * 630 / 1200))).resize((1200, 630), Image.LANCZOS) \
  .save('og-image.jpg', 'JPEG', quality=80, optimize=True, progressive=True)
```

If the stage image's aspect ratio changes, update `.arch { aspect-ratio: 900/1200 }` and the `width`/`height`
attributes on the `<img data-stage>`.

## Design skill (ui-ux-pro-max)

[`.claude/skills/ui-ux-pro-max`](.claude/skills/ui-ux-pro-max) is a Claude Code skill
([nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), MIT) that searches
local CSV data for styles, palettes, font pairings and UX guidelines. It's pure Python with no dependencies and no
network access. You can also run it yourself:

```bash
python .claude/skills/ui-ux-pro-max/scripts/search.py "touch target size" --domain ux
python .claude/skills/ui-ux-pro-max/scripts/search.py "wedding invitation elegant serif" --domain typography
```

Treat its output as suggestions; this README and `CLAUDE.md` win. (For "wedding" it suggests a pink palette and a
SaaS-style page with testimonials — both rejected for this project.)

## Checks before merging

Manual checklist — every change:

- [ ] Page loads with **no console errors**.
- [ ] Countdown is ticking.
- [ ] Stage image shows inside the arch frame; hero stage art renders.
- [ ] "Open in Maps", "Add to calendar" and "Send RSVP via WhatsApp" open the correct links/message.
- [ ] Layout holds at **375px**, **768px** and **1280px** (no horizontal scrolling).
- [ ] Text contrast still ≥ 4.5:1 if colours changed; focus states still visible.
- [ ] Try it with reduced motion on if you touched animation.

Automated version (needs Python + Playwright and an installed Edge or Chrome, or `playwright install chromium`):

```bash
pip install playwright
python -m http.server 8000 &          # in another terminal on Windows
python tools/check.py http://localhost:8000/
```

It reports console errors, countdown ticking, horizontal overflow, image loading and tap targets under 44px at
375/768/1280px, and runs the RSVP flow (empty-name error, then the generated WhatsApp message).

## Deployment

Any static host works.

- **GitHub Pages:** repo **Settings → Pages → Deploy from a branch → `main` / root**. The site will be at
  `https://<user>.github.io/<repo>/`. Note that Pages serves every file in the repo (including `stage.png`, `tools/`
  and `.claude/`); that's harmless — nothing secret is stored here — but those files are publicly reachable.
- **Netlify Drop:** drag a folder containing only `index.html`, `stage.jpg` and `og-image.jpg` onto
  <https://app.netlify.com/drop>.

After deploying: set `og:image` to the absolute URL, paste the link into a WhatsApp chat to check the preview, and
complete [Before launch](#before-launch-open-items).

## Collaboration workflow

- `main` is what gets deployed. Make changes on a branch (`fix/rsvp-copy`, `feat/arabic-dress-code`, …) and open a PR.
- One logical change per PR. Describe what changed and include phone-width screenshots for visual changes.
- Run the [checks](#checks-before-merging) before asking for review.
- **Update this README in the same PR** (relevant section + a [Changelog](#changelog) entry with date, what and why).
- Design decisions (colours, sections, wording) belong to the couple; record them in the [Decision log](#decision-log).
- Hard rules (also in `CLAUDE.md`):
  - Keep everything in `index.html`; no frameworks, build steps or npm.
  - No backend — RSVPs go through WhatsApp.
  - No trackers, analytics or cookie banners.
  - English first, with Arabic alongside (never replacing English).
  - Mobile-first: check 375px before anything else.
- Contributors using **Claude Code** get the project rules automatically from `CLAUDE.md` and the design skill from `.claude/skills/`.

## Decision log

Why things are the way they are. Add new decisions at the bottom.

| Date | Decision | Reason |
|---|---|---|
| 2026-11-14 | Event set to **Sat 21 Nov 2026, 3–7 PM, The Blue View, Engineers Club, Alexandria** | Real event details (the original template said Fri 11 Dec). 7 PM end is an assumption. |
| 2026-11-14 | RSVP deadline **18 November** | The template's 25 November fell after the event. |
| 2026-11-14 | "Our Story" and "Morning Plan" sections removed | Couple's choice; keep the page short. |
| 2026-11-14 | Stage image exported at **900×1200** | The real source is 1086×1448 (3:4), not the 1652×2221 the original spec claimed; the arch frame ratio follows the real image. |
| 2026-11-14 | Redesign direction: **"Refined coastal"** | Chosen over "Classic ivory & gold" and "Modern minimal". |
| 2026-11-14 | Palette: **purple and blue shades** | Couple's request; replaced the original aqua/sand palette. |
| 2026-11-14 | Names in **Great Vibes** script; Arabic names **مؤمن و آلاء** shown under the English | Couple asked about Arabic names; showing both serves both audiences. آلاء is the standard spelling (pending confirmation). |
| 2026-11-14 | Hero uses an **SVG drawing of the venue stage with roses** (not the photo) | Couple's request; the photo is shown once, in the arch frame. |
| 2026-11-14 | Emoji in dress-code tips replaced with **SVG icons** | Consistency and accessibility (ui-ux-pro-max checklist). |
| 2026-11-14 | Skill's pink palette and "testimonials" page pattern **rejected** | Pink is off-brand; testimonials make no sense for an invitation. |
| 2026-11-14 | Decorative "rounded line bundles" background in every section **tried and reverted** | The couple didn't like the look. Don't reintroduce without showing a mock-up first. |

## Changelog

Newest first. Every change to the site adds an entry here.

### 2026-11-14
- **Repo set up for collaboration:** added this README (full context), `.gitignore`, `tools/check.py`, and a rule in
  `CLAUDE.md` to keep this README updated with every change.
- **Reverted** the section-corner line-art background and the line halo behind the hero stage.
- **Redesign** (purple & blue "refined coastal"): new tokens and contrast-checked palette; Great Vibes names + Arabic
  names; SVG stage scene with roses in the hero (generated by `tools/stage-art.py`); arch-topped countdown tiles,
  detail cards and swatches; SVG icons; labelled swatches; 44px+ tap targets; inline RSVP name error; custom select;
  faint arch line drawing behind RSVP and footer; sea fades into the page; installed the `ui-ux-pro-max` skill.
- **Real event details:** names Mo'men & Alaa; Sat 21 Nov 2026 3–7 PM; The Blue View, Engineers Club, Alexandria;
  Maps link; RSVP by 18 November.
- **Launch prep:** optimised `stage.jpg` (2.6 MB PNG → 180 KB JPEG); `og-image.jpg` and Open Graph tags; SVG favicon;
  Google Calendar link includes directions.
- **Accessibility:** labelled form fields, keyboard-accessible radio choices, visible focus states,
  `prefers-reduced-motion` support.
- **Fix:** hero wave layer no longer leaves a gap at the right edge on wide screens.

## Credits and licences

- Fonts via Google Fonts (SIL Open Font License): Great Vibes, Cormorant Garamond, Jost, Amiri.
- `ui-ux-pro-max` skill © 2024 Next Level Builder, MIT licence (see `.claude/skills/ui-ux-pro-max/LICENSE`).
- Stage illustration (`stage.png` and derivatives) provided by the couple for this invitation.
