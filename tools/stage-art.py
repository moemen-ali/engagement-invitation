"""Generates the inline SVG art for index.html: the hero stage scene (central wavy arch + side arches + roses)
-> scene.svg, the arch line drawing -> archline.svg, and the interlocked gold/silver rings -> rings.svg."""
import random, sys

random.seed(21)
DX = 190  # shift central arch into the 1000-wide scene

OUT = [(100, 610), [(112, 540), (70, 470), (92, 400)], [(112, 330), (72, 250), (86, 175)],
       [(92, 112), (130, 84), (180, 86)], [(240, 88), (270, 122), (320, 114)],
       [(370, 106), (410, 70), (460, 74)], [(510, 78), (532, 112), (528, 165)],
       [(522, 245), (550, 315), (532, 395)], [(514, 470), (550, 540), (534, 610)]]
INN = [(186, 610), [(198, 540), (158, 470), (178, 400)], [(196, 335), (160, 262), (172, 214)],
       [(178, 184), (198, 170), (226, 170)], [(268, 172), (296, 194), (330, 188)],
       [(366, 180), (398, 158), (428, 160)], [(452, 162), (450, 192), (447, 222)],
       [(442, 290), (464, 330), (448, 398)], [(432, 470), (464, 540), (448, 610)]]


def p(pt): return f"{pt[0] + DX:g} {pt[1]:g}"


def path(pts, close=""):
    d = f"M{p(pts[0])}" + "".join(f"C{p(a)} {p(b)} {p(c)}" for a, b, c in pts[1:])
    return d + close


def mid(a, b): return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


MID = [mid(OUT[0], INN[0])] + [[mid(x, y) for x, y in zip(s, t)] for s, t in zip(OUT[1:], INN[1:])]
frame = path(OUT) + f"L{p(OUT[0])}Z" + path(INN) + f"L{p(INN[0])}Z"
relief = path(MID)

ROSE = ["#b7a6ee", "#8a70dc", "#9aaaf2", "#ffffff", "#6f8fe0", "#d6cdf7", "#ffffff"]


def bez(s, seg, t):
    a = s[seg - 1] if seg - 1 == 0 else s[seg - 1][2]
    b, c, d = s[seg]
    u = 1 - t
    return tuple(u**3 * a[i] + 3 * u * u * t * b[i] + 3 * u * t * t * c[i] + t**3 * d[i] for i in (0, 1))


def along(segs, n):
    """points on the arch band midline over the given segment numbers"""
    pts = []
    for seg in segs:
        for k in range(n):
            x, y = bez(MID, seg, (k + .5) / n)
            pts.append((x + DX, y))
    return pts


flowers, leaves = [], []


def cluster(pts, spread, big):
    for (x, y) in pts:
        for _ in range(2):
            lx, ly = x + random.uniform(-spread, spread) * 1.3, y + random.uniform(-spread, spread) * 1.3
            leaves.append(f'<use href="#leaf" transform="translate({lx:.0f} {ly:.0f}) rotate({random.randint(0, 359)}) scale({random.uniform(.9, 1.4):.2f})"/>')
        for _ in range(3):
            fx, fy = x + random.uniform(-spread, spread), y + random.uniform(-spread, spread)
            s = random.uniform(*big)
            kind = "rose" if random.random() < .8 else "bloom"
            col = random.choice(ROSE)
            flowers.append(f'<use href="#{kind}" style="color:{col}" transform="translate({fx:.0f} {fy:.0f}) rotate({random.randint(0, 359)}) scale({s:.2f})"/>')


# central arch: top-left corner cascading down the left leg, top-right corner down the right leg
cluster(along([2], 5)[1:] + along([3], 4) + along([4], 3)[:1], 20, (1.15, 1.75))
cluster(along([1], 4)[1:3], 16, (.9, 1.3))
cluster(along([5], 3)[1:] + along([6], 4) + along([7], 5), 20, (1.15, 1.75))
cluster(along([8], 3)[:1], 16, (.9, 1.25))
# side arches: outer flanks
cluster([(70, 262), (52, 310), (44, 360), (46, 410), (56, 460)], 15, (.85, 1.2))
cluster([(930, 262), (948, 310), (956, 360), (954, 410), (944, 460)], 15, (.85, 1.2))

side = ("M40 610V320C40 180 230 180 230 320V610H185V325C185 240 85 240 85 325V610Z"
        "M770 610V320C770 180 960 180 960 320V610H915V325C915 240 815 240 815 325V610Z")

svg = f'''<svg class="scene" overflow="visible" viewBox="0 0 1000 700" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">
  <defs>
    <linearGradient id="seaG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7f9ce8"/><stop offset=".72" stop-color="#3a64c8"/><stop offset="1" stop-color="#f8f7fe"/></linearGradient>
    <linearGradient id="archG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e9e5fb"/></linearGradient>
    <radialGradient id="roseShade"><stop offset=".15" stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#1e1650" stop-opacity=".22"/></radialGradient>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="#2e2766" flood-opacity=".18"/></filter>
    <g id="rose"><g fill="currentColor"><circle cx="0" cy="-8" r="6.5"/><circle cx="7.6" cy="-2.5" r="6.5"/><circle cx="4.7" cy="6.5" r="6.5"/><circle cx="-4.7" cy="6.5" r="6.5"/><circle cx="-7.6" cy="-2.5" r="6.5"/></g><circle r="11" fill="currentColor"/><circle r="11" fill="url(#roseShade)"/>
      <g fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="1.2" stroke-linecap="round">
        <path d="M-2 -1C-2 -4 3 -4 3 -1C3 2-1 3-2 1"/><path d="M-6 0C-6-6 1-8 5-5"/><path d="M6-2C8 3 3 8-2 7"/><path d="M-8 3C-6 8 0 9 3 8"/></g></g>
    <g id="bloom" fill="currentColor"><circle cx="0" cy="-5" r="4.2"/><circle cx="5" cy="-1" r="4.2"/><circle cx="3" cy="5" r="4.2"/><circle cx="-3" cy="5" r="4.2"/><circle cx="-5" cy="-1" r="4.2"/><circle r="2.2" fill="#fff" opacity=".8"/></g>
    <g id="leaf"><path d="M-11 0C-5-6 5-6 11 0C5 6-5 6-11 0Z" fill="#8fae9f"/><path d="M-10 0H9" stroke="#6f9282" stroke-width=".7"/></g>
  </defs>
  <rect x="-3000" y="430" width="7000" height="200" fill="url(#seaG)"/>
  <g class="swell" fill="none" stroke="#fff" stroke-linecap="round" stroke-opacity=".55" stroke-width="2">
    <path d="M-3150 470c60-10 120 10 180 0s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0"/>
    <path d="M-3120 520c60-10 120 10 180 0s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0" stroke-opacity=".4"/>
    <path d="M-3170 570c60-10 120 10 180 0s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0  120 10 180 0 s120-10 180 0" stroke-opacity=".3"/>
  </g>
  <g filter="url(#soft)">
    <path d="{side}" fill="url(#archG)" fill-rule="evenodd" stroke="#cfc6f3" stroke-width="1.5" opacity=".92"/>
    <path d="{frame}" fill="url(#archG)" fill-rule="evenodd" stroke="#cfc6f3" stroke-width="1.5"/>
  </g>
  <path d="{relief}" fill="none" stroke="#d9d2f7" stroke-width="2"/>
  <g>{''.join(leaves)}</g>
  <g>{''.join(flowers)}</g>
  <g fill="#fff" stroke="#d9d2f7" stroke-width="1.5">
    <rect x="20" y="608" width="960" height="44" rx="3"/>
    <rect x="330" y="640" width="340" height="34" rx="3"/>
    <rect x="380" y="668" width="240" height="32" rx="3"/>
  </g>
</svg>'''

line = f'<symbol id="archLine" viewBox="250 60 500 560"><path d="{frame}" fill="none" stroke="currentColor" stroke-width="2"/><path d="{relief}" fill="none" stroke="currentColor" stroke-width="1.2"/></symbol>'

# Hero rings: interlocked gold + silver flat-profile bands (flat top rim, straight sides), seen from slightly above.
RR, RY, BAND, WALL = 60, 18, 22, 6             # outer radius, ellipse squash (ry), band height, rim thickness
RI, RYI = RR - WALL, RY * (RR - WALL) / RR      # inner ellipse
METALS = {
    "gold": dict(face=["#b8892f", "#f6dc95", "#d9ac4f", "#8a6420", "#e9c46d", "#fbe7ae", "#b8892f"],
                 rim=["#f9e8b4", "#e2bd6a"], inner=["#9a7124", "#f1d38a", "#a9802c"]),
    "silver": dict(face=["#8f95a3", "#eef0f5", "#c3c7d1", "#636a79", "#d7dae2", "#f8f9fb", "#8f95a3"],
                   rim=["#fbfbfd", "#cfd3dc"], inner=["#7d8391", "#e7e9ef", "#858b98"]),
}


def stops(cols): return "".join(f'<stop offset="{i / (len(cols) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(cols))


def ring_parts(m, cx, cy):
    """back = inner wall (with see-through hole) + back half of rim; front = front face + front half of rim"""
    face = (f"M{cx - RR} {cy}A{RR} {RY} 0 0 0 {cx + RR} {cy}V{cy + BAND}A{RR} {RY} 0 0 1 {cx - RR} {cy + BAND}Z")
    rim_back = (f"M{cx - RR} {cy}A{RR} {RY} 0 0 1 {cx + RR} {cy}H{cx + RI}A{RI} {RYI:g} 0 0 0 {cx - RI} {cy}Z")
    rim_front = (f"M{cx - RR} {cy}A{RR} {RY} 0 0 0 {cx + RR} {cy}H{cx + RI}A{RI} {RYI:g} 0 0 1 {cx - RI} {cy}Z")
    back = (f'<clipPath id="{m}Open"><ellipse cx="{cx}" cy="{cy}" rx="{RI}" ry="{RYI:g}"/></clipPath>'
            f'<mask id="{m}Hole" maskUnits="userSpaceOnUse" x="0" y="0" width="220" height="110"><rect width="220" height="110" fill="#fff"/>'
            f'<ellipse cx="{cx}" cy="{cy + BAND}" rx="{RI}" ry="{RYI:g}" clip-path="url(#{m}Open)"/></mask>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{RI}" ry="{RYI:g}" fill="url(#{m}In)" mask="url(#{m}Hole)"/>'
            f'<path d="{rim_back}" fill="url(#{m}Rim)"/>')
    front = f'<path d="{face}" fill="url(#{m}Face)"/><path d="{rim_front}" fill="url(#{m}Rim)"/>'
    return back, front, face


GC, SC = (72, 38), (140, 46)
g_back, g_front, _ = ring_parts("gold", *GC)
s_back, s_front, s_face = ring_parts("silver", *SC)


def crossings():
    """x of the front and back points where the two bands cross (circle intersection in top view, y = depth * RY/RR)"""
    k = RY / RR
    (x1, z1), (x2, z2) = (GC[0], GC[1] / k), (SC[0], SC[1] / k)
    dx, dz = x2 - x1, z2 - z1
    d = (dx * dx + dz * dz) ** .5
    h = (RR * RR - (d / 2) ** 2) ** .5
    mx, mz, px, pz = (x1 + x2) / 2, (z1 + z2) / 2, -dz / d, dx / d
    a, b = (mx + px * h, mz + pz * h), (mx - px * h, mz - pz * h)
    front, back = (a, b) if a[1] > b[1] else (b, a)
    return front[0], back[0]


X_FRONT, X_BACK = crossings()
defs = "".join(
    f'<linearGradient id="{m}Face" x1="0" x2="1">{stops(c["face"])}</linearGradient>'
    f'<linearGradient id="{m}Rim" x1="0" y1="0" x2="0" y2="1">{stops(c["rim"])}</linearGradient>'
    f'<linearGradient id="{m}In" x1="0" x2="1">{stops(c["inner"])}</linearGradient>' for m, c in METALS.items())
# where the gold band passes through the silver ring, the silver front face covers it (right-hand crossing only)
defs += (f'<clipPath id="rightHalf"><rect x="{X_FRONT:.1f}" y="0" width="160" height="110"/></clipPath>'
         f'<clipPath id="pastBack"><rect x="{X_BACK:.1f}" y="0" width="160" height="110"/></clipPath>'
         '<mask id="goldBehind" maskUnits="userSpaceOnUse" x="0" y="0" width="220" height="110"><rect width="220" height="110" fill="#fff"/>'
         f'<path d="{s_face}" clip-path="url(#rightHalf)"/></mask>'
         '<filter id="ringShadow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>')
rings = (f'<svg class="rings" viewBox="0 12 212 94" role="img" aria-label="Gold and silver engagement rings">'
         f'<defs>{defs}</defs>'
         f'<ellipse cx="106" cy="92" rx="88" ry="8" fill="#2e2766" opacity=".14" filter="url(#ringShadow)"/>'
         f'{g_back}{s_back}<g clip-path="url(#pastBack)">{g_back.split("</mask>", 1)[1]}</g>'
         f'{s_front}<g mask="url(#goldBehind)">{g_front}</g></svg>')

open(sys.argv[1] + "/scene.svg", "w", encoding="utf-8").write(svg)
open(sys.argv[1] + "/rings.svg", "w", encoding="utf-8").write(rings)
open(sys.argv[1] + "/archline.svg", "w", encoding="utf-8").write(line)
open(sys.argv[1] + "/preview.html", "w", encoding="utf-8").write(
    '<body style="margin:0;background:linear-gradient(#ece8fc,#d9e2fa)"><div style="width:100%;aspect-ratio:1000/700">'
    + svg.replace('class="scene"', 'style="width:100%;height:100%"') + '</div></body>')
print(len(svg), "bytes;", len(flowers), "flowers")
