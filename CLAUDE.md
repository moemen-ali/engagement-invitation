# Mo'men & Alaa — Engagement Invitation Website

A single-page invitation website for an open-air engagement party by the sea.
The party is at 4 PM on Saturday 21 November 2026, Cairo time (UTC+02:00),
at **The Blue View, Engineers Club, Alexandria** ([Maps](https://maps.app.goo.gl/B5Ygc689t4PCkwjm6)).

## Keep README.md up to date (required)

`README.md` is the full project context for human collaborators on GitHub. **Every change you make to this repo
must update it in the same change**:
- Update every README section the change affects (event details, open items, layout, how it works, editing guide,
  sections, design system, art, images, checks, deployment, workflow).
- Add a dated entry at the top of its **Changelog** (date, what changed, why).
- If the change reflects a decision by the couple (design, wording, sections, details), add a row to the **Decision log**.
- When a "Before launch" item is done, tick it off; when a new one appears, add it.
- If this file (`CLAUDE.md`) gains or changes a rule, mirror it in the README where collaborators need it.

Don't say a change is done until README.md reflects it.

## Files

```
.
├── CLAUDE.md      ← this file (rules for Claude Code)
├── README.md      ← full project context for collaborators — keep it updated (see above)
├── .gitignore
├── index.html     ← the whole site: markup, CSS and JS in one file
├── stage.jpg      ← illustrated venue stage art, optimized (portrait, 900×1200, ~180 KB)
├── og-card.jpg    ← link preview (designed card), made by tools/og-card.py — re-run it after changing CONFIG
├── couple.webp    ← bride & groom illustration (Countdown section), cut out by tools/couple-art.py
├── invitation-2.png ← generated couple illustration (source of couple.webp; prompt in README). Not used by the page
├── invitation.jfif ← printed invitation card: reference image only. Not used by the page
├── stage.png      ← original source art (1086×1448, 2.6 MB). Not used by the page; don't ship it
├── tools/stage-art.py          ← generates the hero's inline SVG stage art (see "Hero art" below). Not shipped
├── tools/check.py              ← automated browser checks (Playwright). Not shipped
├── tools/og-card.py            ← renders og-card.jpg from CONFIG + page art (Playwright). Not shipped
├── tools/couple-art.py         ← cuts couple.webp out of invitation-2.png (Pillow + NumPy). Not shipped
└── .claude/skills/ui-ux-pro-max ← design-intelligence skill (MIT, nextlevelbuilder/ui-ux-pro-max-skill). Not shipped
```

- Keep the site **self-contained in `index.html`**. No build step, no framework, no npm.
- The only external dependency is Google Fonts (Italianno, Cormorant Garamond, Jost, Amiri).
- If the stage image is renamed or converted (e.g. to `.webp`), update `CONFIG.stageImage`.

## Editing content

All event details live in the `CONFIG` object at the bottom of `index.html`:
names (English and Arabic: `name1Ar`/`name2Ar`), start/end time, venue, address, Maps URL and stage image path.
**Change event details only there.** The page fills them in through `data-*` attributes such as `data-name1` and `data-venue`.
Never hard-code these values in the markup.

- **Exception:** the `<meta name="description">` and `og:*` tags in `<head>` repeat the date and venue as static text,
  because WhatsApp's link preview doesn't run JavaScript. Keep them in sync with `CONFIG` when details change.
- Times use ISO strings with the `+02:00` offset, and all formatting uses `timeZone: 'Africa/Cairo'`.
  Guests may open the link from abroad, so keep it that way.

## Sections (in order)

1. **Hero**: lavender sky gradient, soft sun glow (top right), festoon string lights, interlocked gold + silver flat-profile rings (SVG), names in script with the Arabic names below, Arabic invite line, date, then the SVG stage scene (wavy central arch + two side arches with cascading roses, in front of a blue sea with drifting swell lines).
2. **Countdown**: the couple illustration (`couple.webp`) on a lavender venue-arch panel, then venue-arch tiles with days, hours, minutes and seconds to `CONFIG.start`.
   The dress is **white**; the groom's suit is **dark charcoal grey** (both confirmed).
3. **Stage ("Under the Arches")**: `stage.jpg` in a venue-arch frame. The frame's aspect ratio matches the image (900/1200), so update it if the image changes.
4. **Details**: three venue-arch cards with SVG icons (When / Time / Where), a Maps link and an "Add to calendar" button (Google Calendar link).
5. **Dress code ("Coastal Chic")**: labelled palette swatches and tip pills with SVG icons.
6. **Footer**: names (script + Arabic), the Arabic line "في انتظاركم", the date, and the faint arch line drawing.

The "Our Story" and "Morning Plan" timeline sections and the **RSVP** (hero button + form) were **intentionally removed**.
Do not add them back.

## Design system

The theme is coastal, airy and romantic, in **purple and blue shades** (chosen by the couple):
lavender sky, periwinkle and violet roses, sea blue water, white sculptural arches.
The stage photo keeps its natural colours; everything around it uses the tokens below.

| Token      | Value     | Use                                         |
|------------|-----------|---------------------------------------------|
| `--violet` | `#6a4cc4` | primary accent, buttons, eyebrows           |
| `--indigo` | `#2e2766` | headings, names, hover                      |
| `--blue`   | `#3a64c8` | sea, swatch                                 |
| `--peri`   | `#9aaaf2` | periwinkle accents, roses                   |
| `--lilac`  | `#d9d2f7` | borders, line art                           |
| `--mist`   | `#efedfc` | alternate section background                |
| `--pearl`  | `#f8f7fe` | main background                             |
| `--glow`   | `#f3d9a4` | sun glow and bulbs only (use sparingly)     |
| `--ink`    | `#262249` | body text                                   |
| `--soft`   | `#585482` | secondary text                              |

- **Contrast:** all text pairs above are ≥ 4.5:1 (soft on lilac is the tightest at 4.8:1). Re-check if you change a token.
- **Names:** Italianno (script), only for the couple's names; capitals must read as capitals (Great Vibes was dropped
  because its M and A look lowercase). The `&` is Cormorant italic in violet.
- **Headings:** Cormorant Garamond (400, italic for accents).
- **Body and labels:** Jost 300 at 1rem. Labels are 500 weight, uppercase, wide letter-spacing, never smaller than .75rem.
- **Arabic:** Amiri, with `direction: rtl` (`.ar` class).
- **Shapes:** the photo frame, couple panel, countdown tiles and detail cards use the **venue-arch frame** (the stage's
  central-arch silhouette: `.frame` + `.frame-line` + `.frame-shape.venue`, `--venue-arch` mask, `#venueArch` symbol,
  `--frame-gap` for the outline offset — see README "Venue-arch frame"). Any new framed image, panel or card must use it,
  not a generic rounded shape. Simple rounded-top arches only for the small swatches and favicon; soft waves in the hero.
  Reuse these motifs rather than adding new ones.
- **Icons:** inline stroke SVGs (`.icon`, 24px grid, 1.6 stroke), `aria-hidden="true"`. No emoji as icons.
- **Touch:** buttons and links are at least 44px tall.
- **Motion:** gentle only. This means scroll reveal (`.reveal` → `.in`, only when JS runs), drifting sea swell and glowing bulbs.
  All of it is switched off under `prefers-reduced-motion`. Do the same for any animation you add.
- A printed invitation card exists, but it's **only an art source**: never take event details from it
  (its venue wording and name order differ on purpose). `CONFIG` is the source of truth.
- Don't use dark or night themes, sunset oranges as a main color, or pink and red accents
  (keep roses on the blue side of lavender).

### Hero art

The stage scene in the hero is inline SVG generated by `tools/stage-art.py`
(arch shapes, rose/bloom/leaf shapes, colours and placement; seeded, so output is stable).
To change it, edit the script, run `python tools/stage-art.py <out-dir>`, and replace the
`<svg class="scene">…</svg>` block and the `archLine` symbol in `index.html` with `scene.svg` and `archline.svg`.
The same script makes the hero rings (`rings.svg` → the `<svg class="rings">…</svg>` block): flat-profile bands
(flat top, straight sides — never domed), gold left, silver right, interlocked at computed crossing points.
Gold/silver appear only in the rings; don't spread gold into the UI.
On phones the scene is cropped to the central arch (`preserveAspectRatio="xMidYMax slice"` in a square box);
on wider screens it shows all three arches at `min(56svh, 620px)` tall.

## Design skill

`.claude/skills/ui-ux-pro-max` is installed for design work. Run its search from the repo root, e.g.
`python .claude/skills/ui-ux-pro-max/scripts/search.py "touch target size" --domain ux`.
Treat its output as suggestions: the rules in this file win (it suggests pink palettes and SaaS page
patterns for "wedding", which don't apply here).

## Rules for changes

- The site is mobile-first, because most guests will open it from WhatsApp on a phone.
  Check layouts at 375px width before anything else.
- Keep text in English, with the existing Arabic lines.
  If asked to make the site bilingual, add Arabic alongside rather than replacing English.
- Optimize images before shipping: the stage image should be ≤ 400 KB.
  Export it as WebP or JPEG at about 80% quality and roughly 1200px tall.
- Keep accessibility basics: an `alt` on images, accessible names on controls, and visible focus states.
- Don't add trackers, analytics or cookie banners unless asked.
- Don't add a backend, forms or an RSVP (the couple removed RSVP on purpose).

## Preview and checks

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

Automated: `python tools/check.py http://localhost:8000/` (needs `pip install playwright` + Edge/Chrome).
It covers everything below except visual judgement, so also look at the page at 375px.

Before saying a change is done, check all of the following:
- The page loads with no console errors.
- The countdown is ticking.
- The stage image shows inside the arch.
- "Open in Maps" and "Add to calendar" open the correct links.
- The layout holds at 375px, 768px and 1280px widths.
- README.md is updated (sections + Changelog).

## Deploy

Static hosting works. The simplest options are:
- **Netlify Drop:** drag the folder onto app.netlify.com/drop.
- **GitHub Pages (chosen, https://moemen-ali.github.io/engagement-invitation/):** Settings → Pages → deploy from `main` / root. Pages serves every file in the repo
  (including `stage.png`, `tools/`, `.claude/`); that's harmless, but never commit secrets.

Before sharing the link:
- `og:url` and `og:image` are absolute URLs on `https://moemen-ali.github.io/engagement-invitation/` (WhatsApp ignores relative image URLs).
  If the site moves, change both. After changing names, date/time, venue, rings or the stage photo, re-run
  `python tools/og-card.py og-card.jpg` and keep the `<head>` description/og text in sync.
- The favicon is an inline SVG data URI in `<head>`: the venue's central arch with roses, generated by `tools/stage-art.py`
  (`favicon-uri.txt`). Encode `#` as `%23` in data URIs.
- For Netlify Drop, upload only `index.html`, `stage.jpg`, `couple.webp` and the link-preview image in use.

## Git

Remote: <https://github.com/moemen-ali/engagement-invitation> (`origin`).

- `main` is what gets deployed. Work on a branch and open a PR; one logical change per PR.
- Commit or push only when the user asks.
