# Mo'men & Alaa — Engagement Invitation Website

A single-page, mobile-first invitation website for **Mo'men & Alaa's** open-air engagement party by the sea.
Guests open the link (mostly from WhatsApp on a phone), see the date, venue and dress code, and RSVP through WhatsApp.

- **Stack:** one static `index.html` (HTML + CSS + vanilla JS). No framework, no build step, no npm, no backend.
- **Repository:** <https://github.com/moemen-ali/engagement-invitation>
- **Live site:** <https://moemen-ali.github.io/engagement-invitation/> (GitHub Pages — live once Pages is enabled, see [Before launch](#before-launch-open-items))

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
| Time | 4:00 PM – 7:00 PM, Cairo time (UTC+02:00) |
| Venue | The Blue View, Engineers Club, Alexandria |
| Map | <https://maps.app.goo.gl/B5Ygc689t4PCkwjm6> (pin at 31.239241, 29.953164 on the Corniche) |
| Setting | Open air, on grass, white sculpted arches with flowers, sea behind the stage |
| RSVP deadline | 18 November |
| RSVP channel | WhatsApp message to the number in `CONFIG.whatsapp` |

All of these values live in one place: the `CONFIG` object at the bottom of `index.html` (see [Editing guide](#editing-guide-common-tasks)).

## Before launch: open items

These must be done before the link is sent to guests:

- [ ] **WhatsApp number.** `CONFIG.whatsapp` is still the placeholder `201000000000`, so RSVPs go nowhere.
      Format: country code + number, no `+`, no spaces, no leading zero (e.g. `2010XXXXXXXX`).
- [ ] **Enable GitHub Pages:** repo **Settings → Pages → Deploy from a branch → `main` / `/ (root)`**. The page's
      `og:url` and `og:image` already point at `https://moemen-ali.github.io/engagement-invitation/`; if you host elsewhere, change both.
- [ ] **Check the WhatsApp preview** once live: paste the link into a chat and confirm the card image appears.
- [x] Link-preview image: the designed card (`og-card.jpg`) with an absolute URL.
- [ ] **Arabic spelling of Alaa.** The site uses **آلاء** (the standard spelling). If the family writes it الاء,
      change `CONFIG.name2Ar`.
- [ ] **End time.** 7:00 PM was assumed (no end time was given). Change `CONFIG.end` if needed.
- [ ] Add the live URL at the top of this file.

## Quick start

```bash
git clone https://github.com/moemen-ali/engagement-invitation.git
cd engagement-invitation
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
├── og-card.jpg                   ← link preview: designed invitation card (1200×630, ~93 KB), from tools/og-card.py
├── couple.webp                   ← bride & groom illustration for the Countdown section (786×1200, ~95 KB, transparent)
├── stage.png                     ← original source art (1086×1448, 2.6 MB). Not used by the page
├── invitation.jfif               ← printed invitation card (736×1104) — style/pose reference only. Not used by the page
├── invitation-2.png              ← AI-generated couple illustration (1024×1536) — source of couple.webp. Not used by the page
├── tools/
│   ├── stage-art.py              ← generates the hero's inline SVG: stage scene, arch line drawing, rings
│   ├── og-card.py                ← renders og-card.jpg from CONFIG + the page's art (Playwright)
│   ├── couple-art.py             ← cuts couple.webp out of invitation-2.png's flat background (Pillow + NumPy)
│   └── check.py                  ← automated browser checks (see "Checks before merging")
├── .claude/skills/ui-ux-pro-max/ ← design-intelligence skill for Claude Code (MIT)
├── CLAUDE.md                     ← rules for Claude Code (AI assistant) working in this repo
├── README.md                     ← this file: full project context for collaborators
└── .gitignore
```

Only `index.html`, `stage.jpg`, `og-card.jpg` and `couple.webp` are needed by the live site. The only external dependency is Google Fonts.

## How the page works

### Content binding

`index.html` contains **no hard-coded event details** in the markup. Elements carry empty `data-*` attributes and a
small script fills them from `CONFIG` on load:

| Attribute | Filled with |
|---|---|
| `data-name1`, `data-name2` | English names |
| `data-names-ar` | `"<name1Ar> و <name2Ar>"` |
| `data-when` | `Saturday · 21 November 2026 · 4:00 PM` |
| `data-weekday`, `data-date-long` | `Saturday`, `21 November 2026` |
| `data-time`, `data-until` | `4:00 PM`, `Until 7:00 PM` |
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

Times are ISO strings with the `+02:00` offset (`2026-11-21T16:00:00+02:00`), and every date/time is formatted
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
    start: "2026-11-21T16:00:00+02:00",   // Saturday 21 Nov 2026, 4:00 PM Cairo time
    end: "2026-11-21T19:00:00+02:00",
    venue: "The Blue View",
    address: "Engineers Club, Alexandria",
    mapsUrl: "https://maps.app.goo.gl/B5Ygc689t4PCkwjm6",
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

1. **Hero** — lavender sky gradient, soft sun glow (top right), festoon string lights with glowing bulbs; a pair of
   **interlocked gold and silver rings** (flat-profile bands, SVG); eyebrow
   "Together with their families"; names in Great Vibes script with a Cormorant `&`; Arabic names (Amiri); Arabic invite
   line «بكل الحب ندعوكم لمشاركتنا فرحة خطوبتنا»; "Invite you to a seaside engagement celebration"; date line;
   **Kindly RSVP** button (jumps to `#rsvp`); then the **SVG stage scene** (see [Hero stage art](#hero-stage-art-svg-generator)).
2. **Countdown** — the **couple illustration** (`couple.webp`: bride in a white gown, groom in a dark grey suit, seen
   from behind) on a lavender panel cut to the **venue-arch shape**, then "Until we meet by the sea" and four arch-topped tiles (Days, Hours,
   Mins, Secs) also cut to the venue-arch shape. Two columns from 860px (drawing left, countdown right); stacked on phones (drawing first).
3. **Under the Arches** — short venue paragraph + `stage.jpg` in a **venue-arch frame** (white border and lilac outline
   ring that follow the central arch's wavy silhouette).
   Two columns from 860px wide (text left, photo right), stacked on phones.
4. **The Details** — three venue-arch cards with SVG icons: When / Time / Where (+ "Open in Maps"), then an
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

**Motifs:** the **venue arch** — the real silhouette of the stage's central arch (wavy top that dips in the middle,
wavy sides) — shapes the photo frame, the couple panel, the countdown tiles and the detail cards (see
[Venue-arch frame](#venue-arch-frame)) and the favicon (the central arch with roses); simple rounded-top arches only
for the small swatches; soft waves in the hero. Reuse these rather than
inventing new shapes.

**Icons:** inline stroke SVGs (`.icon`: 24px grid, 1.6 stroke, round caps), `aria-hidden="true"`, next to visible text.
No emoji as icons.

**Interaction & accessibility**

- Buttons, inputs, choices and links are ≥ 44px tall; form text is 1rem so iOS Safari doesn't zoom on focus.
- Visible focus: 2px indigo outline on links/buttons, violet ring on inputs, outline on the focused radio choice.
- Every form field has a `<label>`; the attending choice is a `<fieldset>` labelled by its heading; radios are
  visually hidden but keyboard-accessible.
- Images have `alt`; decorative SVGs are `aria-hidden`; swatches have visible names (not colour-only).

**Motion:** gentle only — scroll reveal (0.7s), sea swell drift (10s), bulb glow (3.2s). All off under reduced motion.

**Ring metals:** the rings are the one place gold and silver appear (gold `#b8892f`–`#fbe7ae`,
silver `#636a79`–`#f8f9fb`). Don't spread gold into the UI — `--glow` stays limited to the sun and bulbs.

**Don't:** dark/night themes, sunset orange as a main colour, pink or red accents (keep roses on the blue side of lavender).

## Hero stage art (SVG generator)

All inline SVG art in the hero comes from [`tools/stage-art.py`](tools/stage-art.py): the **stage scene**, the
**arch line drawing** and the **rings**.

### Stage scene

The hero's stage scene is inline SVG modelled on the real venue stage: a **wavy central arch** with a raised relief line,
two plain **side arches**, ~100 **roses/blooms** with sage leaves cascading down the arches (lavender `#b7a6ee`, violet
`#8a70dc`, periwinkle `#9aaaf2`, blue `#6f8fe0`, pale lilac, white), a blue **sea band** with drifting white swell lines
that fades into the page, and a white **stage platform** with steps.

It is produced by the script (seeded random, so the output is stable):

```bash
python tools/stage-art.py out/          # writes out/scene.svg, out/archline.svg, out/rings.svg, out/preview.html
```

Then replace in `index.html`:
- the `<svg class="scene" …>…</svg>` block with `scene.svg`;
- the `<symbol id="archLine" …>…</symbol>` (inside the hidden sprite at the top of `<body>`) with `archline.svg`
  — this is the faint arch line drawing used behind the RSVP form and footer;
- the `<svg class="rings" …>…</svg>` block (top of the hero `.intro`) with `rings.svg`.

`preview.html` lets you look at the art on its own first. Layout rules:
- Phones (≤ 640px): the scene sits in a square box with `preserveAspectRatio="xMidYMax slice"`, so it crops to the central arch.
- Wider screens: height `min(56svh, 620px)` at the full 1000×700 ratio, showing all three arches.
- The SVG has `overflow="visible"` so the sea band runs the full viewport width (the hero clips it).

### Rings

Two interlocked **flat-profile bands** (flat top rim, straight vertical sides — not domed), modelled on a plain
gold wedding band: **gold** on the left, **silver** on the right, seen from slightly above with a soft shadow.
Each band is built from an elliptical top rim, a front face with a vertical metallic gradient (highlights plus a
dark streak) and an inner back wall, with a see-through opening.

The interlock is geometrically correct: the script intersects the two rings' circles in top view to find the front
and back crossing points, and swaps which band is in front exactly there (gold passes behind the silver front face
and in front of its back wall; the silver's left side shows inside the gold ring). Change size/spacing via
`RR`, `RY`, `BAND`, `WALL` and the centres `GC`/`SC`; colours via `METALS`.

In the page the SVG is `.rings` (`width: clamp(118px, 30vw, 160px)`), `role="img"` with
`aria-label="Gold and silver engagement rings"`.

### Venue-arch frame

Images and illustration panels are framed by the **silhouette of the venue's central arch**, so they echo the real
stage instead of a generic rounded shape. `tools/stage-art.py` derives it from the same `OUT` curve as the hero art,
normalised to a 0–100 box, and writes:

- `frame-symbol.svg` → the `<symbol id="venueArch">` in the hidden sprite (used for the lilac outline ring);
- `frame-mask.css.txt` → the value of the `--venue-arch` CSS variable (a data-URI SVG mask).

Markup pattern (stretches to any size):

```html
<div class="frame arch">                                  <!-- size the frame -->
  <svg class="frame-line" aria-hidden="true" focusable="false"><use href="#venueArch" width="100%" height="100%" /></svg>
  <div class="frame-shape venue"> … </div>               <!-- .venue = masked to the arch silhouette -->
</div>
```

Used for:

| Element | Fill | Outline gap (`--frame-gap`) |
|---|---|---|
| Stage photo `.arch` | white 10px border, photo also masked | 10px (default) |
| Couple panel `.couple-frame` | lavender gradient, illustration on top | 10px |
| Countdown tiles `.unit` | white | 5px |
| Detail cards `.card` | white | 7px |

Notes:
- Content inside a frame is lifted above the shape by `.frame > :where(:not(.frame-shape):not(.frame-line))
  { position: relative }` — `:where()` keeps it at zero specificity so elements like `.couple` can still be absolute.
- `.frame` centres itself with `margin: 0 auto`; grid items override it (`.unit.frame, .card.frame { margin: 0 }`)
  or they'd shrink to their content.
- `.frame-line` needs `max-width: none` (it's larger than the frame by 2 × `--frame-gap`).
- Shadows use `filter: drop-shadow(...)` on the frame so they follow the wavy silhouette.

## Couple drawing

`couple.webp` is the bride-and-groom illustration shown in the Countdown section: bride in a **white** gown, groom in a
**dark charcoal grey** suit, seen from behind (both colours confirmed by the couple).

**How it was made.** The printed card's drawing (`invitation.jfif`) was too small and pink to reuse directly, so a new
illustration (`invitation-2.png`, 1024×1536) was generated with an image tool, attaching the card as the reference
image, using this prompt:

```text
Using the attached invitation card as the reference for pose, composition and drawing style, create ONLY the bride and groom illustration, isolated on its own.

Subject: a bride and groom seen from behind, standing side by side, full body. Bride on the left, groom on the right. Both heads turned gently toward each other so their faces show in soft profile, exactly as in the reference.

Bride: long, soft, wavy brown hair worn half-up with a small delicate floral hair clip; off-the-shoulder top with small ruffled sleeves; a thin belt at the waist; a long, flowing A-line tulle gown with a wide sweeping train and a softly scalloped hem. The dress is PURE WHITE (clean bright white, not pink, not cream, not blush). Delicate embroidered sprigs on the lower skirt in very light silver-grey.

Groom: short, neat brown hair; a tailored DARK CHARCOAL GREY suit (jacket and matching trousers, color around #3A3D45), with a hint of a white shirt collar. Hands relaxed at his sides.

Style: elegant hand-drawn fine-line ink illustration with a soft watercolor wash, romantic and minimal, like a luxury wedding invitation. Crisp, continuous, clean outlines in dark charcoal-indigo ink, smooth even line weight, no sketchy broken strokes. Soft light shading only.

Background: completely plain, flat, solid pale lavender (#E4E2FB), with no texture, no paper grain, no vignette, no gradient, no shadow on the ground.

Framing: vertical portrait 2:3, high resolution (at least 1600 px tall). The whole couple fully in frame, from the top of the groom's head to the end of the dress train, with even empty margin on all sides. Nothing cropped.
```

Negative prompt: `text, letters, names, dates, typography, flowers around the couple, floral frame, leaves, branches, lanterns, candles, rings, gold glitter, gold splashes, watercolor blobs or stains in the background, paper texture, pink dress, blush dress, cream dress, beige suit, light suit, black suit, faces toward the viewer, extra people, cropped train, cropped head, blurry lines, broken lines, smudges, frame, border, watermark`

**Cut-out.** [`tools/couple-art.py`](tools/couple-art.py) removes the flat lavender background:

```bash
pip install pillow numpy
python tools/couple-art.py invitation-2.png couple.webp
```

- Background = background-coloured pixels connected to the image border (flood fill), so nothing inside the figures
  is removed; soft alpha on the edge band with the lavender un-mixed (no halo); stray specks dropped.
- Trimmed, scaled to 1200 px tall, WebP with alpha (~95 KB).
- Shown at the bottom of the `.couple-frame` panel (`height: 84%`), with descriptive `alt`.

To change the illustration, generate a new image with the same prompt (flat `#E4E2FB`-ish background), save it as
`invitation-2.png` and re-run the script.

## Images

| File | Size | Use |
|---|---|---|
| `stage.png` | 1086×1448, 2.6 MB | original source art — keep it, edit/export from it |
| `stage.jpg` | 900×1200, ~180 KB, JPEG q80 progressive | stage section photo (must stay ≤ 400 KB) |
| `og-card.jpg` | 1200×630, ~93 KB | WhatsApp / social link preview (designed card) — see [Link preview](#link-preview) |
| `couple.webp` | 786×1200, ~95 KB, WebP with alpha | couple illustration in the Countdown section (see above) |
| `invitation-2.png` | 1024×1536, PNG | generated couple illustration — source for `couple.webp` |
| `invitation.jfif` | 736×1104, JPEG | printed card — reference image for the generation only; its event details are **not** used |

To regenerate `stage.jpg` from the source (requires Pillow), then re-render the preview card (it embeds the photo):

```python
from PIL import Image
im = Image.open('stage.png').convert('RGB')
im.resize((900, 1200), Image.LANCZOS).save('stage.jpg', 'JPEG', quality=80, optimize=True, progressive=True)
```

If the stage image's aspect ratio changes, update `.arch { aspect-ratio: 900/1200 }` and the `width`/`height`
attributes on the `<img data-stage>`.

## Favicon

An inline SVG data URI in `<head>`: the venue's **central arch** (wavy, with its opening) in lilac with a violet
outline, and roses on its corners like the stage. Generated by `tools/stage-art.py` → `favicon-uri.txt`; paste it into
`<link rel="icon" type="image/svg+xml" href="…">`. (When building data URIs, `#` must be encoded as `%23`.)

## Link preview

What WhatsApp (and other apps) show when the link is shared comes from the `og:*` tags in `<head>`: title, description
and a 1200×630 image. WhatsApp doesn't run JavaScript, so these are static text — keep them in sync with `CONFIG`.

The image is **`og-card.jpg`**, a designed card: the stage photo in the venue-arch frame on the left; the rings,
"Mo'men & Alaa", the Arabic names, the date/time and the venue on the right, on the site's lavender. It tells guests
whose event, when and where right in the chat, before they tap.

```bash
python tools/og-card.py og-card.jpg     # reads CONFIG, the rings SVG and the --venue-arch mask from index.html
```

**Re-run it whenever names, date/time, venue, the rings or the stage photo change**, and commit the new image.

`og:image` and `og:url` are absolute (`https://moemen-ali.github.io/engagement-invitation/…`) because WhatsApp ignores relative image URLs.
WhatsApp caches previews per link, so after changing the image an already-shared link may keep the old preview for a while.

(An earlier plain crop of the stage photo, `og-image.jpg`, was replaced by the card and removed.)

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
- [ ] Stage image shows inside the arch frame; hero stage art, rings and the couple drawing render.
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

- **GitHub Pages (chosen):** repo **Settings → Pages → Deploy from a branch → `main` / root**. The site will be at
  <https://moemen-ali.github.io/engagement-invitation/>. Note that Pages serves every file in the repo (including `stage.png`, `tools/`
  and `.claude/`); that's harmless — nothing secret is stored here — but those files are publicly reachable.
- **Netlify Drop:** drag a folder containing only `index.html`, `stage.jpg`, `couple.webp` and `og-card.jpg` onto
  <https://app.netlify.com/drop> — and change `og:url`/`og:image` to the Netlify address.

After deploying: paste the link into a WhatsApp chat to check the preview, and complete
[Before launch](#before-launch-open-items).

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
| 2026-11-14 | **Interlocked gold + silver flat-profile rings** at the top of the hero | Couple's request, modelled on a plain flat gold band (not rounded). |
| 2026-11-14 | **Couple drawing** from the invitation card placed in the **Countdown** section | A couple looking ahead suits "Until we meet by the sea", and it was the sparsest section. RSVP (pushes the form down on phones) and footer (low visibility) were rejected. |
| 2026-11-14 | Dress **white**; suit **outline only** | Couple's instruction — the suit colour wasn't confirmed yet. (Superseded below.) |
| 2026-11-14 | Couple drawing **regenerated** (`invitation-2.png`) with a **dark grey suit**; auto-traced line art dropped | The line art traced from the small card looked broken; suit colour confirmed as dark grey. |
| 2026-11-14 | Images and panels framed by the **venue's central-arch silhouette** instead of generic rounded arches | Couple's request: custom shapes that match the venue stage (like the RSVP line drawing). |
| 2026-11-14 | Maps link changed to `B5Ygc689t4PCkwjm6` | Couple's updated link (same spot on the Corniche, a few metres away). |
| 2026-11-14 | A separate printed invitation card is used **only as an art source** — its venue wording ("The Open Air Hall", Gleem) and name order ("Alaa & Mo'men") are **not** used | Couple's instruction: keep The Blue View and "Mo'men & Alaa". (The start time was later confirmed as 4 PM, matching the card.) |
| 2026-11-14 | Start time changed to **4:00 PM** (end still 7:00 PM, assumed) | Couple's correction. |
| 2026-11-14 | Link preview = the **designed card** (`og-card.jpg`), absolute URL on GitHub Pages; `og-image.jpg` removed | The card shows whose event, when and where in the chat; still features the venue stage. Hosting on GitHub Pages (https://moemen-ali.github.io/engagement-invitation/). |
| 2026-11-14 | Countdown tiles and detail cards also use the **venue-arch shape** | Couple's request: everything framed should match the venue stage. |

## Changelog

Newest first. Every change to the site adds an entry here.

### 2026-11-14
- **Favicon** redrawn as the venue's central arch with roses (generated by `tools/stage-art.py`).
- **Link preview:** now the designed card `og-card.jpg` (rendered by `tools/og-card.py`), with absolute `og:image`
  and `og:url` on https://moemen-ali.github.io/engagement-invitation/; removed `og-image.jpg`. `tools/check.py` checks og:image is absolute and present.
- **Start time is now 4:00 PM** (`CONFIG.start`, `<head>` description and `og:description`); end stays 7:00 PM.
- **Venue-arch tiles and cards:** countdown tiles and detail cards now use the venue-arch silhouette with an outline
  ring (`--frame-gap` per element); fixed frame CSS so grid items fill their columns and the couple stays inside its panel.
- **Couple illustration replaced:** `couple.webp` is now cut out of the generated `invitation-2.png` (white dress, dark
  grey suit; prompt recorded under [Couple drawing](#couple-drawing)); `tools/couple-art.py` rewritten as a
  background cut-out.
- **Venue-arch frames:** the stage photo and the couple panel are now shaped like the venue's central arch
  (`--venue-arch` mask + `#venueArch` outline, generated by `tools/stage-art.py`).
- **Couple drawing:** added `couple.webp` (from the invitation card via `tools/couple-art.py`: indigo line art, white
  dress, outlined suit) in a lavender arch beside/above the countdown.
- **Maps link** updated to <https://maps.app.goo.gl/B5Ygc689t4PCkwjm6>.
- **Repository** published at <https://github.com/moemen-ali/engagement-invitation>.
- **Rings:** added interlocked gold and silver flat-profile rings (SVG) above "Together with their families" in the
  hero; generated by `tools/stage-art.py` (`rings.svg`) with geometrically computed crossings.
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
