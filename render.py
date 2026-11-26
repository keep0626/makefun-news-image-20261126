#!/usr/bin/env python3
"""Draw Thursday 26 November 2026's world news as one 1024x1024 page.

Reads stories.json next to this file and writes entry.png beside it.
Deterministic: no randomness, no clock, no network. Pillow only.
Layout is measured from the wrapped text, so nothing can run off the page.
"""

import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (26, 26, 26)
RED = (179, 35, 27)
NAVY = (31, 58, 95)
TEAL = (15, 91, 77)
GOLD = (184, 134, 11)
GREY = (90, 86, 78)
LINE = (180, 172, 152)


def font(name, size):
    paths = {
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "serif_r": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "serif_i": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    }
    try:
        return ImageFont.truetype(paths[name], size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- art panels
def art_panel(draw, kind, x, y, w, h):
    """Flat hand-drawn-style pictogram for one story. All shapes drawn here.
    Short panels (cards) get a compact variant that fits inside h."""
    bg = {"bank": (31, 58, 95), "chart": (15, 91, 77), "missile": (60, 30, 40),
          "mine": (74, 52, 28), "storm": (38, 54, 74), "phone": (31, 58, 95),
          "flag": (255, 252, 244), "chess": (60, 58, 90), "ipo": (15, 91, 77)}[kind]
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w / 2, y + h / 2
    compact = h <= 64
    if kind == "bank":
        draw.polygon([(cx - 52, cy - 18), (cx + 52, cy - 18), (cx, cy - 42)], fill=(232, 196, 90))
        for i in range(5):
            px = cx - 44 + i * 22
            draw.rectangle([px, cy - 14, px + 10, cy + 30], fill=(248, 243, 230))
        draw.rectangle([cx - 56, cy + 30, cx + 56, cy + 38], fill=(232, 196, 90))
        draw.text((cx + 62, cy - 34), "%", font=font("serif", 44), fill=(232, 196, 90))
    elif kind == "chart":
        draw.rectangle([x + 14, y + h - 26, x + w - 14, y + h - 18], fill=(248, 243, 230))
        pts = [(x + 20, cy + 34), (x + 48, cy + 10), (x + 74, cy + 22),
               (x + 100, cy - 8), (x + 128, cy - 26)]
        draw.line(pts, fill=(232, 196, 90), width=5)
        for px, py in pts:
            draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(255, 252, 244))
        draw.polygon([(x + 128, cy - 26), (x + 118, cy - 12), (x + 138, cy - 16)],
                     fill=(232, 196, 90))
    elif kind == "missile":
        draw.polygon([(cx, cy - 52), (cx + 14, cy - 18), (cx + 14, cy + 18),
                      (cx, cy + 34), (cx - 14, cy + 18), (cx - 14, cy - 18)],
                     fill=(248, 243, 230))
        draw.polygon([(cx - 14, cy + 18), (cx - 30, cy + 38), (cx - 14, cy + 30)], fill=(179, 35, 27))
        draw.polygon([(cx + 14, cy + 18), (cx + 30, cy + 38), (cx + 14, cy + 30)], fill=(179, 35, 27))
        draw.polygon([(cx - 6, cy + 34), (cx, cy + 56), (cx + 6, cy + 34)], fill=(232, 196, 90))
    elif kind == "mine":
        if compact:
            draw.arc([cx - 42, cy - 16, cx + 42, cy + 20], 180, 360,
                     fill=(232, 196, 90), width=4)
            draw.line([cx - 42, cy + 20, cx - 42, cy + 25], fill=(232, 196, 90), width=4)
            draw.line([cx + 42, cy + 20, cx + 42, cy + 25], fill=(232, 196, 90), width=4)
            draw.line([cx - 30, cy + 23, cx + 30, cy - 8], fill=(248, 243, 230), width=3)
            draw.line([cx - 30, cy - 8, cx + 30, cy + 23], fill=(248, 243, 230), width=3)
        else:
            draw.arc([cx - 46, cy - 34, cx + 46, cy + 44], 180, 360, fill=(232, 196, 90), width=5)
            draw.line([cx - 46, cy + 44, cx - 46, cy + 52], fill=(232, 196, 90), width=5)
            draw.line([cx + 46, cy + 44, cx + 46, cy + 52], fill=(232, 196, 90), width=5)
            draw.arc([cx - 26, cy - 8, cx + 26, cy + 34], 180, 360, fill=(248, 243, 230), width=4)
            draw.line([cx - 40, cy + 52, cx + 40, cy + 6], fill=(248, 243, 230), width=4)
            draw.line([cx - 40, cy + 6, cx + 40, cy + 52], fill=(248, 243, 230), width=4)
    elif kind == "storm":
        if compact:
            draw.ellipse([cx - 48, cy - 12, cx - 4, cy + 4], fill=(248, 243, 230))
            draw.ellipse([cx - 22, cy - 20, cx + 28, cy + 0], fill=(248, 243, 230))
            draw.ellipse([cx + 8, cy - 10, cx + 48, cy + 4], fill=(220, 214, 200))
            for rx in (-34, -12, 10, 30):
                draw.line([cx + rx, cy + 8, cx + rx - 3, cy + 22], fill=(232, 196, 90), width=3)
            draw.polygon([(cx + 54, cy - 16), (cx + 46, cy + 2), (cx + 53, cy + 2),
                          (cx + 46, cy + 18), (cx + 60, cy - 2), (cx + 53, cy - 2)],
                         fill=(232, 196, 90))
        else:
            draw.ellipse([cx - 52, cy - 26, cx - 6, cy + 6], fill=(248, 243, 230))
            draw.ellipse([cx - 26, cy - 40, cx + 30, cy - 2], fill=(248, 243, 230))
            draw.ellipse([cx + 6, cy - 22, cx + 52, cy + 6], fill=(220, 214, 200))
            for rx in (-38, -12, 14, 38):
                draw.line([cx + rx, cy + 16, cx + rx - 6, cy + 40], fill=(232, 196, 90), width=4)
            draw.polygon([(cx + 52, cy - 30), (cx + 38, cy + 2), (cx + 50, cy + 2),
                          (cx + 38, cy + 30), (cx + 62, cy - 8), (cx + 50, cy - 8)],
                         fill=(232, 196, 90))
    elif kind == "phone":
        if compact:
            draw.rounded_rectangle([cx - 22, cy - 24, cx + 22, cy + 24], radius=5,
                                   fill=(248, 243, 230))
            draw.rectangle([cx - 17, cy - 18, cx + 17, cy - 12], fill=(31, 58, 95))
            for r in range(2):
                for c in range(3):
                    gx, gy = cx - 18 + c * 13, cy - 8 + r * 12
                    draw.rounded_rectangle([gx, gy, gx + 10, gy + 10], radius=2,
                                           fill=(15, 91, 77) if (r + c) % 2 else (179, 35, 27))
            draw.text((cx - 6, cy + 14), "$", font=font("serif", 13), fill=(179, 35, 27))
        else:
            draw.rounded_rectangle([cx - 34, cy - 52, cx + 34, cy + 52], radius=10,
                                   fill=(248, 243, 230))
            draw.rectangle([cx - 26, cy - 40, cx + 26, cy - 30], fill=(31, 58, 95))
            for r in range(2):
                for c in range(3):
                    gx, gy = cx - 24 + c * 18, cy - 18 + r * 20
                    draw.rounded_rectangle([gx, gy, gx + 13, gy + 13], radius=3,
                                           fill=(15, 91, 77) if (r + c) % 2 else (179, 35, 27))
            draw.text((cx - 13, cy + 22), "$", font=font("serif", 26), fill=(179, 35, 27))
    elif kind == "flag":
        draw.rectangle([x + 18, y + 8, x + w - 18, y + h // 3 + 3], fill=(255, 153, 51))
        draw.rectangle([x + 18, y + h // 3 + 3, x + w - 18, y + 2 * h // 3], fill=(255, 255, 255))
        draw.rectangle([x + 18, y + 2 * h // 3, x + w - 18, y + h - 8], fill=(19, 136, 8))
        r = min(16, h // 3)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 56, 120), width=2)
        for a in range(0, 360, 30):
            t = math.radians(a)
            draw.line([cx, cy, cx + (r - 2) * math.cos(t), cy + (r - 2) * math.sin(t)],
                      fill=(0, 56, 120), width=1)
    elif kind == "chess":
        sq = 8 if compact else 26
        n = 6 if compact else 4
        for r in range(n):
            for c in range(n):
                fill = (248, 243, 230) if (r + c) % 2 == 0 else (26, 26, 26)
                draw.rectangle([cx - n * sq / 2 + c * sq, cy - n * sq / 2 + r * sq,
                                cx - n * sq / 2 + (c + 1) * sq, cy - n * sq / 2 + (r + 1) * sq],
                               fill=fill)
        draw.rectangle([cx - n * sq / 2, cy - n * sq / 2, cx + n * sq / 2, cy + n * sq / 2],
                       outline=(232, 196, 90), width=2)
        draw.text((cx - n * sq / 2 + 1, cy - n * sq / 2 + 1), "K",
                  font=font("serif", 16 if compact else 40), fill=(179, 35, 27))
    elif kind == "ipo":
        if compact:
            draw.rectangle([cx - 40, cy + 4, cx - 16, cy + 24], fill=(248, 243, 230))
            draw.rectangle([cx - 10, cy - 8, cx + 14, cy + 24], fill=(232, 196, 90))
            draw.rectangle([cx + 20, cy - 20, cx + 40, cy + 24], fill=(248, 243, 230))
            draw.line([cx - 44, cy + 8, cx - 10, cy - 10, cx + 8, cy + 2, cx + 44, cy - 20],
                      fill=(179, 35, 27), width=3)
        else:
            draw.rectangle([cx - 44, cy - 6, cx - 16, cy + 44], fill=(248, 243, 230))
            draw.rectangle([cx - 8, cy - 26, cx + 20, cy + 44], fill=(232, 196, 90))
            draw.rectangle([cx + 28, cy - 44, cx + 48, cy + 44], fill=(248, 243, 230))
            draw.line([cx - 48, cy + 10, cx - 10, cy - 14, cx + 10, cy + 2, cx + 52, cy - 40],
                      fill=(179, 35, 27), width=5)
            draw.polygon([(cx + 52, cy - 40), (cx + 38, cy - 40), (cx + 52, cy - 26)],
                         fill=(179, 35, 27))


# ---------------------------------------------------------------- world map
CONTINENTS = {
    "n_america": [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-85, 66),
                  (-75, 72), (-60, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26),
                  (-90, 21), (-97, 16), (-105, 20), (-117, 33), (-125, 40), (-125, 49),
                  (-140, 60), (-155, 58), (-165, 60)],
    "s_america": [(-80, 10), (-60, 8), (-50, 0), (-40, -5), (-35, -10), (-40, -20),
                  (-48, -28), (-58, -35), (-65, -41), (-70, -50), (-73, -53), (-70, -40),
                  (-70, -20), (-77, -12), (-80, 0)],
    "europe": [(-10, 36), (0, 36), (3, 43), (8, 44), (12, 44), (18, 40), (23, 36),
               (28, 36), (30, 41), (28, 45), (23, 45), (19, 45), (12, 46), (5, 48),
               (0, 48), (-2, 49), (-5, 50), (-10, 54), (-8, 58), (-5, 60), (5, 60),
               (10, 58), (18, 56), (21, 55), (24, 58), (30, 60), (30, 66), (25, 70),
               (18, 69), (12, 66), (5, 58)],
    "africa": [(-17, 15), (-10, 5), (-8, 4), (9, 4), (13, -1), (12, -6), (13, -12),
               (12, -18), (16, -23), (19, -29), (20, -35), (26, -34), (33, -26),
               (35, -20), (40, -15), (40, -10), (46, -11), (51, -11), (51, 2),
               (48, 11), (43, 12), (39, 15), (37, 18), (33, 27), (32, 31), (20, 32),
               (11, 34), (0, 36), (-6, 35), (-10, 31), (-15, 27), (-17, 21)],
    "asia": [(30, 66), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75),
             (100, 76), (110, 76), (120, 73), (130, 72), (140, 72), (150, 70),
             (160, 69), (170, 66), (178, 65), (170, 60), (162, 56), (158, 52),
             (150, 59), (142, 50), (140, 45), (135, 43), (130, 42), (127, 40),
             (122, 38), (120, 32), (118, 25), (110, 20), (108, 12), (105, 9),
             (100, 8), (97, 10), (94, 17), (91, 22), (89, 22), (86, 20), (80, 15),
             (77, 8), (75, 10), (72, 20), (68, 22), (66, 25), (62, 25), (58, 26),
             (56, 27), (52, 27), (50, 29), (48, 30), (44, 29), (40, 31), (36, 36),
             (33, 36), (30, 41), (28, 41), (30, 45), (32, 42), (35, 44), (38, 46),
             (40, 47), (42, 46), (45, 48), (48, 50), (50, 52), (55, 55), (60, 58),
             (65, 60), (70, 63), (75, 65)],
    "oceania": [(113, -22), (114, -30), (115, -35), (120, -34), (126, -32), (129, -32),
                (132, -32), (135, -35), (137, -38), (140, -38), (142, -39), (146, -39),
                (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
                (142, -11), (136, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
}


def draw_map(draw, x, y, w, h, stories):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 230, 238))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    for pts in CONTINENTS.values():
        poly = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h) for lon, lat in pts]
        draw.polygon(poly, fill=(226, 214, 178), outline=(150, 140, 118))
    # numbered pins for placed stories (skip n=8: no verified venue)
    for s in stories:
        if s["n"] == 8:
            continue
        px = x + (s["lon"] + 180) / 360 * w
        py = y + (90 - s["lat"]) / 180 * h
        r = 8
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
        tw = draw.textlength(str(s["n"]), font=font("sans_b", 10))
        draw.text((px - tw / 2, py - 6), str(s["n"]), font=font("sans_b", 10),
                  fill=(255, 255, 255))
    draw.text((x + 6, y + h - 16), "PINS 1-7, 9 = PICTURED STORIES",
              font=font("sans_b", 9), fill=NAVY)


# ---------------------------------------------------------------- page
def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as f:
        d = json.load(f)

    img = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(img)
    mx = 24
    cw = W - 2 * mx  # 976

    # kicker
    y = 12
    center(dr, y, d["kicker"], font("sans_b", 15), RED)
    y += 20
    # masthead: the date is the biggest element
    center(dr, y, "Thursday 26 November 2026", font("serif", 54), INK)
    y += 62
    dr.line([mx, y, W - mx, y], fill=INK, width=2)
    y += 7
    center(dr, y, d["subdeck"], font("serif_i", 16), RED)
    y += 23

    # region bar: segments sized by story count, labels inside only when they fit
    total = sum(r["count"] for r in d["regions"])
    rx = mx
    for r in d["regions"]:
        seg = int(cw * r["count"] / total)
        dr.rectangle([rx, y, rx + seg, y + 22], fill=r["color"])
        label = "%s %d" % (r["name"], r["count"])
        tw = dr.textlength(label, font=font("sans_b", 11))
        if tw < seg - 6:
            dr.text((rx + (seg - tw) / 2, y + 5), label, font=font("sans_b", 11),
                    fill=(255, 255, 255))
        rx += seg
    y += 26
    # legend line so the small segments are still named
    lx = mx
    for r in d["regions"]:
        dr.rectangle([lx, y + 2, lx + 9, y + 11], fill=r["color"])
        lx += 13
        label = "%s %d" % (r["name"], r["count"])
        dr.text((lx, y), label, font=font("sans_b", 10), fill=INK)
        lx += int(dr.textlength(label, font=font("sans_b", 10))) + 16
    y += 16

    # numbers strip: six big red figures
    nw = cw // 6
    for i, nb in enumerate(d["numbers"]):
        x0 = mx + i * nw
        dr.rectangle([x0 + 2, y, x0 + nw - 2, y + 52], outline=LINE, width=1)
        center(dr, y + 4, nb["figure"], font("serif", 23), RED, x0 + 2, x0 + nw - 2)
        center(dr, y + 34, nb["label"], font("sans_b", 8), GREY, x0 + 2, x0 + nw - 2)
    y += 60

    # leads: three columns with big picture panels, height measured per column
    colw = (cw - 2 * 14) // 3
    lead_top = y
    lead_bottom = y
    for i, s in enumerate(d["leads"]):
        x0 = mx + i * (colw + 14)
        art_panel(dr, s["art"], x0, y, colw, 104)
        yy = y + 112
        dr.ellipse([x0, yy, x0 + 18, yy + 18], fill=RED)
        tw = dr.textlength(str(s["n"]), font=font("sans_b", 12))
        dr.text((x0 + (18 - tw) / 2, yy + 2), str(s["n"]), font=font("sans_b", 12),
                fill=(255, 255, 255))
        dr.text((x0 + 24, yy + 3), s["tag"], font=font("sans_b", 11), fill=NAVY)
        yy += 24
        for line in wrap(dr, s["headline"], font("serif", 20), colw):
            dr.text((x0, yy), line, font=font("serif", 20), fill=INK)
            yy += 24
        yy += 2
        for line in wrap(dr, s["deck"], font("sans", 12), colw):
            dr.text((x0, yy), line, font=font("sans", 12), fill=(50, 48, 44))
            yy += 15
        yy += 4
        dr.text((x0, yy), s["source"], font=font("sans_b", 10), fill=RED)
        lead_bottom = max(lead_bottom, yy + 12)
    y = lead_bottom + 6
    dr.line([mx, y, W - mx, y], fill=LINE, width=1)
    y += 8

    # picture cards: 3 x 2, row height measured
    for row in range(2):
        row_bottom = y
        for col in range(3):
            s = d["cards"][row * 3 + col]
            x0 = mx + col * (colw + 14)
            yy = y
            art_panel(dr, s["art"], x0, yy, colw, 50)
            yy += 56
            dr.ellipse([x0, yy, x0 + 15, yy + 15], fill=RED)
            tw = dr.textlength(str(s["n"]), font=font("sans_b", 10))
            dr.text((x0 + (15 - tw) / 2, yy + 2), str(s["n"]), font=font("sans_b", 10),
                    fill=(255, 255, 255))
            dr.text((x0 + 20, yy + 2), s["tag"], font=font("sans_b", 10), fill=NAVY)
            yy += 19
            for line in wrap(dr, s["headline"], font("serif", 15), colw):
                dr.text((x0, yy), line, font=font("serif", 15), fill=INK)
                yy += 18
            for line in wrap(dr, s["deck"], font("sans", 11), colw):
                dr.text((x0, yy), line, font=font("sans", 11), fill=(50, 48, 44))
                yy += 13
            row_bottom = max(row_bottom, yy)
        y = row_bottom + 8
    dr.line([mx, y, W - mx, y], fill=LINE, width=1)
    y += 8

    # bottom zone: map + numbered briefs (one line each by construction)
    zone_top = y
    map_w = 330
    map_h = 150
    draw_map(dr, mx, y, map_w, map_h, d["leads"] + d["cards"])
    bx = mx + map_w + 14
    bw = W - mx - bx
    dr.text((bx, y), "ALSO ON THURSDAY 26 NOVEMBER",
            font=font("sans_b", 12), fill=RED)
    half = (len(d["briefs"]) + 1) // 2
    cols = [d["briefs"][:half], d["briefs"][half:]]
    col_w = bw // 2
    briefs_bottom = y + 18
    for ci, col in enumerate(cols):
        cx = bx + ci * col_w
        cy = y + 18
        for b in col:
            num = "%d." % b["n"]
            dr.text((cx, cy), num, font=font("sans_b", 11), fill=RED)
            nw_ = dr.textlength(num + " ", font=font("sans_b", 11))
            lines = wrap(dr, b["text"], font("sans", 11), col_w - nw_ - 6)
            for j, line in enumerate(lines):
                dr.text((cx + nw_, cy + j * 12), line, font=font("sans", 11), fill=INK)
            cy += 12 * max(1, len(lines))
        briefs_bottom = max(briefs_bottom, cy)
    y = max(zone_top + map_h, briefs_bottom) + 6

    # DATE CHECK box, sized to its wrapped lines
    lines = wrap(dr, d["date_check"], font("sans", 10), cw - 16)
    box_h = 22 + 11 * len(lines)
    dr.rectangle([mx, y, W - mx, y + box_h], outline=RED, width=2)
    dr.text((mx + 8, y + 5), "DATE CHECK", font=font("sans_b", 11), fill=RED)
    yy = y + 20
    for line in lines:
        dr.text((mx + 8, yy), line, font=font("sans", 10), fill=INK)
        yy += 11
    y += box_h + 6

    # footer
    center(dr, y, "SOURCES: REUTERS · KCNA · UN NEWS · THE HINDU BUSINESSLINE · CHESS · PRESS REPORTS, 26 NOV 2026  |  CONFIRMED = ON THE RECORD · REPORTED = AS REPORTED",
           font("sans", 9), GREY)
    y += 12
    if y > H:
        raise SystemExit("layout overflow: final y=%d" % y)

    img.save(os.path.join(HERE, "entry.png"), optimize=True)


if __name__ == "__main__":
    main()
