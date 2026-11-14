"""Extracts the bride-and-groom drawing from the printed invitation card as transparent line art for the site.

    python tools/couple-art.py [invitation.jfif] [couple.webp]

- Keeps only what's inside a hand-traced outline of the couple (drops the card's text, florals, gold, sage wash).
- Pencil lines -> indigo ink (#2e2766) with anti-aliased alpha (local-contrast line detection, green leaves skipped).
- The bride's dress (pink watercolour on the card) -> a soft white wash. The groom's suit stays outline only
  (its colour isn't confirmed yet; when it is, add a fill the same way as DRESS_FILL).
- Output is upscaled 2x for sharper lines and saved as WebP with alpha.
Requires Pillow and NumPy.
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = sys.argv[1] if len(sys.argv) > 1 else "invitation.jfif"
OUT = sys.argv[2] if len(sys.argv) > 2 else "couple.webp"
BOX = (355, 318, 736, 1054)          # crop box in card pixels (card is 736x1104)
SCALE = 2
INK = (46, 39, 102)                  # --indigo

# outline of both figures, in card pixels (clockwise from the groom's head)
COUPLE = [(570, 345), (585, 325), (610, 322), (630, 340), (632, 370), (625, 395), (650, 410), (690, 430), (700, 470),
          (705, 520), (708, 600), (700, 630), (672, 640), (670, 700), (668, 800), (690, 860), (712, 930), (736, 985),
          (736, 1020), (700, 1035), (640, 1045), (560, 1050), (470, 1050), (400, 1045), (368, 1030), (362, 1005),
          (378, 985), (392, 950), (405, 900), (420, 860), (428, 820), (438, 760), (452, 700), (470, 650), (490, 610),
          (500, 590), (490, 570), (482, 540), (475, 525), (480, 505), (490, 470), (495, 440), (503, 410), (515, 397),
          (535, 397), (552, 415), (560, 430), (568, 420), (575, 400), (568, 375)]
# groom's side (jacket + legs right of the dress train): never filled - the suit stays outline only
GROOM = [(565, 318), (640, 318), (640, 400), (736, 420), (736, 990), (700, 940), (670, 870), (640, 790), (615, 700),
         (592, 645), (580, 600), (577, 420)]
# skirt silhouette (solid white base under the card's pink wash, so the dress reads evenly white)
SKIRT = [(505, 585), (555, 580), (585, 640), (615, 700), (640, 790), (670, 870), (700, 940), (736, 990), (736, 1020),
         (700, 1035), (640, 1045), (560, 1050), (470, 1050), (400, 1045), (368, 1030), (366, 1005), (382, 980),
         (400, 935), (418, 880), (436, 820), (455, 750), (475, 680), (492, 625)]
# leftover twig marks from the card's florals (centre x, centre y, radius) - erased
ERASE = [(664, 648, 12), (683, 853, 8)]
# bodice + sleeves (white like the skirt; the skirt itself is found from the card's pink wash)
BODICE = [(478, 522), (495, 512), (520, 515), (545, 515), (556, 528), (556, 560), (552, 580), (510, 584), (500, 560)]


def poly_mask(points, size):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).polygon([((x - BOX[0]) * SCALE, (y - BOX[1]) * SCALE) for x, y in points], fill=255)
    return np.asarray(m, dtype=np.float32) / 255


card = Image.open(SRC).convert("RGB").crop(BOX)
big = card.resize((card.width * SCALE, card.height * SCALE), Image.LANCZOS)
rgb = np.asarray(big, dtype=np.float32)
r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b

inside = poly_mask(COUPLE, big.size)
inside = np.asarray(Image.fromarray((inside * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), np.float32) / 255

# lines: darker than their local surroundings; ignore green (leaves) strokes
bg = np.asarray(Image.fromarray(lum.astype(np.uint8)).filter(ImageFilter.GaussianBlur(7)), np.float32)
strength = np.clip((bg - lum - 6) / 34, 0, 1)
not_green = np.clip(1 - (g - r - 2) / 10, 0, 1)
line_a = strength * not_green * inside
# drop thick filled blobs (the card's leaves) on the groom's right side; real lines are thin strokes
dark = Image.fromarray((strength > .45).astype(np.uint8) * 255)
blobs = np.asarray(dark.filter(ImageFilter.MinFilter(7)).filter(ImageFilter.MaxFilter(15)), np.float32) / 255
xs = np.arange(lum.shape[1]) / SCALE + BOX[0]
line_a *= 1 - blobs * (xs[None, :] > 640)
yy, xx = np.mgrid[0:lum.shape[0], 0:lum.shape[1]] / SCALE
for ex, ey, er in ERASE:
    line_a *= np.clip((np.hypot(xx + BOX[0] - ex, yy + BOX[1] - ey) - er) / 2, 0, 1)
line_a *= 0.9

# dress: the card's pink wash, smoothed into a soft white fill (+ bodice)
pink = np.clip(((r - b) - 14) / 22, 0, 1) * np.clip(((r - g) - 4) / 14, 0, 1)
pink = np.asarray(Image.fromarray((pink * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5)), np.float32) / 255
bodice = np.asarray(Image.fromarray((poly_mask(BODICE, big.size) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), np.float32) / 255
groom = np.asarray(Image.fromarray((poly_mask(GROOM, big.size) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4)), np.float32) / 255
skirt = np.asarray(Image.fromarray((poly_mask(SKIRT, big.size) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(8)), np.float32) / 255
DRESS_FILL = np.clip(np.maximum.reduce([np.clip(pink * 1.6, 0, 1), skirt * .9, bodice]) * inside * (1 - groom), 0, 1) * 0.92

# composite: white dress under indigo lines
a = line_a + DRESS_FILL * (1 - line_a)
out_rgb = np.empty_like(rgb)
for i, ink in enumerate(INK):
    out_rgb[..., i] = (ink * line_a + 255 * DRESS_FILL * (1 - line_a)) / np.maximum(a, 1e-6)
out = np.dstack([out_rgb, a * 255]).clip(0, 255).astype(np.uint8)
img = Image.fromarray(out, "RGBA")
img = img.crop(img.getbbox())
img.save(OUT, "WEBP", quality=82, alpha_quality=70, method=6)
print(OUT, img.size)
