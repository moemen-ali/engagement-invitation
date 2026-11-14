"""Cuts the bride-and-groom illustration out of its flat lavender background for the site.

    python tools/couple-art.py [invitation-2.png] [couple.webp]

The source (`invitation-2.png`) was generated from the printed invitation card with the prompt recorded in README.md
("Couple drawing"): white dress, dark charcoal suit, on a flat pale-lavender background.

- Background = pixels close to the background colour that are connected to the image border (flood fill), so
  white/lavender-ish areas inside the figures are never removed.
- A soft alpha ramp on the edge band, with the lavender un-mixed out of semi-transparent edge pixels (no halo).
- Isolated specks not connected to the figures are dropped.
- Trimmed to the figures, scaled to TARGET_H tall, saved as WebP with alpha.
Requires Pillow and NumPy.
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = sys.argv[1] if len(sys.argv) > 1 else "invitation-2.png"
OUT = sys.argv[2] if len(sys.argv) > 2 else "couple.webp"
TARGET_H = 1200          # px; shown at up to 440 CSS px tall, so this covers 2x+ screens
BG_TOL = 9               # colour distance still counted as flat background
EDGE_LO, EDGE_HI = 3, 19  # alpha ramp (colour distance) on the edge band
MARK = (255, 0, 255)

src = Image.open(SRC).convert("RGB")
rgb = np.asarray(src, np.float32)
h, w = rgb.shape[:2]
border = np.concatenate([rgb[:8].reshape(-1, 3), rgb[-8:].reshape(-1, 3), rgb[:, :8].reshape(-1, 3), rgb[:, -8:].reshape(-1, 3)])
bg = np.median(border, axis=0)
dist = np.linalg.norm(rgb - bg, axis=2)

# flood-fill the background from every border pixel that is background-coloured
filled = src.copy()
seeds = [(x, y) for x in range(0, w, 16) for y in (0, h - 1)] + [(x, y) for y in range(0, h, 16) for x in (0, w - 1)]
for x, y in seeds:
    if dist[y, x] < BG_TOL and filled.getpixel((x, y)) != MARK:
        ImageDraw.floodfill(filled, (x, y), MARK, thresh=BG_TOL)
is_bg = np.all(np.asarray(filled) == MARK, axis=2)

# soft edge: in a thin band next to the background, alpha follows colour distance
near = np.asarray(Image.fromarray(is_bg.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5)), bool)
band = near & ~is_bg
alpha = np.ones((h, w), np.float32)
alpha[is_bg] = 0
alpha[band] = np.clip((dist[band] - EDGE_LO) / (EDGE_HI - EDGE_LO), 0, 1)

# drop stray specks: keep only pixels connected to the couple (seeded at the image centre)
solid = Image.fromarray((alpha > 0).astype(np.uint8) * 255).copy()  # copy: arrays-backed images ignore floodfill
ImageDraw.floodfill(solid, (w // 2, h // 2), 128)
alpha[np.asarray(solid) != 128] = 0

# un-mix the lavender from semi-transparent edge pixels
a3 = alpha[..., None]
fg = np.where(a3 > 0.01, (rgb - (1 - a3) * bg) / np.maximum(a3, 0.01), 0)
out = Image.fromarray(np.dstack([fg.clip(0, 255), alpha * 255]).astype(np.uint8), "RGBA")
out = out.crop(out.getbbox())
out = out.resize((round(out.width * TARGET_H / out.height), TARGET_H), Image.LANCZOS)
out.save(OUT, "WEBP", quality=84, alpha_quality=90, method=6)
print(OUT, out.size, "background", bg.astype(int).tolist())
