#!/usr/bin/env python3
"""news-image-20261125: draw one front page summing up 25 November 2026.

Pure standard library. Draws a 1024x1024 newspaper front page
("THE WORLD TODAY") with six stories from Wednesday 25 November 2026
and writes it as a deterministic PNG to /output/entry.png when
/output exists, otherwise ./entry.png.
"""

import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (252, 250, 244)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
LIGHT_BLUE = (120, 170, 220)
GREY = (110, 110, 108)
DARK_GREY = (70, 70, 68)
GOLD = (176, 132, 40)
GREEN = (34, 110, 60)
YELLOW = (235, 190, 40)
BROWN = (120, 70, 20)
NAVY = (24, 32, 64)

# ---------------------------------------------------------------- font 5x7
# Each glyph: 7 rows of 5 bits, '1' = ink.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
}


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_text(img, x, y, text, scale, color):
    """Draw upper-cased text; returns x just past the last glyph."""
    text = text.upper()
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    fill_rect(img, cx + col * scale, y + row * scale,
                              scale, scale, color)
        cx += 6 * scale
    return cx


def draw_text_centered(img, cx, y, text, scale, color):
    w = text_width(text, scale)
    draw_text(img, cx - w // 2, y, text, scale, color)


def wrap_text(text, scale, max_width):
    """Greedy word wrap; returns list of lines fitting max_width."""
    words = text.upper().split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------- canvas
def new_image():
    img = bytearray(W * H * 3)
    for i in range(0, len(img), 3):
        img[i] = PAPER[0]
        img[i + 1] = PAPER[1]
        img[i + 2] = PAPER[2]
    return img


def set_pixel(img, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        img[i] = color[0]
        img[i + 1] = color[1]
        img[i + 2] = color[2]


def fill_rect(img, x, y, w, h, color):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        for xx in range(x0, x1):
            i = base + (xx - x0) * 3
            img[i] = color[0]
            img[i + 1] = color[1]
            img[i + 2] = color[2]


def draw_hline(img, x, y, w, color, thick=1):
    fill_rect(img, x, y, w, thick, color)


def draw_vline(img, x, y, h, color, thick=1):
    fill_rect(img, x, y, thick, h, color)


def draw_line(img, x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        set_pixel(img, x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def draw_rect_outline(img, x, y, w, h, color, thick=1):
    fill_rect(img, x, y, w, thick, color)
    fill_rect(img, x, y + h - thick, w, thick, color)
    fill_rect(img, x, y, thick, h, color)
    fill_rect(img, x + w - thick, y, thick, h, color)


def fill_circle(img, cx, cy, r, color):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                set_pixel(img, xx, yy, color)


def fill_triangle(img, ax, ay, bx, by, cx, cy, color):
    min_y = min(ay, by, cy)
    max_y = max(ay, by, cy)
    for y in range(min_y, max_y + 1):
        xs = []
        for (px, py, qx, qy) in ((ax, ay, bx, by), (bx, by, cx, cy),
                                (cx, cy, ax, ay)):
            if py == qy:
                continue
            if min(py, qy) <= y < max(py, qy) or (y == max_y and y == max(py, qy)):
                t = (y - py) / (qy - py)
                xs.append(px + t * (qx - px))
        if len(xs) >= 2:
            x0 = int(min(xs))
            x1 = int(max(xs))
            for x in range(x0, x1 + 1):
                set_pixel(img, x, y, color)


def fill_poly(img, points, color):
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    n = len(points)
    for y in range(min_y, max_y + 1):
        xs = []
        for i in range(n):
            px, py = points[i]
            qx, qy = points[(i + 1) % n]
            if py == qy:
                continue
            if min(py, qy) <= y < max(py, qy) or (y == max_y and y == max(py, qy)):
                t = (y - py) / (qy - py)
                xs.append(px + t * (qx - px))
        if len(xs) >= 2:
            for x in range(int(min(xs)), int(max(xs)) + 1):
                set_pixel(img, x, y, color)


# ---------------------------------------------------------------------- PNG
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(img, path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += img[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# -------------------------------------------------------------- pictograms
def pic_ship_fire(img, x, y, w, h):
    """Russian cargo ship Sparta II burning in the Gulf of Finland."""
    sea_y = y + h - 26
    fill_rect(img, x, sea_y, w, 26, LIGHT_BLUE)
    for i in range(0, w, 26):
        draw_line(img, x + i, sea_y + 6, x + i + 13, sea_y + 12, BLUE)
        draw_line(img, x + i + 13, sea_y + 12, x + i + 26, sea_y + 6, BLUE)
    # hull
    fill_poly(img, [(x + 8, sea_y - 26), (x + w - 8, sea_y - 26),
                    (x + w - 26, sea_y), (x + 26, sea_y)], (90, 40, 30))
    # containers
    fill_rect(img, x + 22, sea_y - 62, 52, 36, RED)
    fill_rect(img, x + 78, sea_y - 62, 52, 36, BLUE)
    fill_rect(img, x + 134, sea_y - 62, 52, 36, GOLD)
    for cx0 in (22, 78, 134):
        draw_rect_outline(img, x + cx0, sea_y - 62, 52, 36, INK, 2)
    # smoke plume above the containers
    fill_circle(img, x + 100, sea_y - 78, 14, GREY)
    fill_circle(img, x + 118, sea_y - 96, 12, DARK_GREY)
    fill_circle(img, x + 104, sea_y - 112, 10, GREY)
    # flames licking the deck
    fill_triangle(img, x + 40, sea_y - 60, x + 52, sea_y - 84,
                  x + 64, sea_y - 60, YELLOW)
    fill_triangle(img, x + 150, sea_y - 60, x + 160, sea_y - 80,
                  x + 170, sea_y - 60, YELLOW)
    # drone above, top right
    dx, dy = x + w - 70, y + 14
    fill_rect(img, dx, dy, 26, 10, INK)
    draw_hline(img, dx - 10, dy - 4, 46, INK, 3)
    fill_circle(img, dx - 8, dy - 4, 4, DARK_GREY)
    fill_circle(img, dx + 34, dy - 4, 4, DARK_GREY)
    draw_vline(img, dx + 13, dy + 10, 12, INK, 2)


def pic_cyber(img, x, y, w, h):
    """Monitor with a warning triangle: unclassified systems breached."""
    # monitor
    mx, my = x + 10, y + 6
    mw, mh = w - 20, 40
    fill_rect(img, mx, my, mw, mh, NAVY)
    draw_rect_outline(img, mx, my, mw, mh, INK, 3)
    # warning triangle
    cx = x + w // 2
    ty = my + 5
    fill_triangle(img, cx - 20, ty + 30, cx, ty, cx + 20, ty + 30, YELLOW)
    draw_text(img, cx - 3, ty + 13, "!", 1, INK)
    # stand, kept short so the label below stays clear
    fill_rect(img, cx - 3, my + mh, 6, 8, INK)
    fill_rect(img, cx - 20, my + mh + 8, 40, 4, INK)
    # label at the bottom
    draw_text_centered(img, cx, y + h - 14, "UNCLASSIFIED", 1, RED)


def pic_tower(img, x, y, w, h):
    """Riyadh's PIF tower, tapered, with a damage patch and a drone."""
    cx = x + w // 2
    base_y = y + h - 6
    # tapered tower
    fill_poly(img, [(cx - 18, y + 6), (cx + 18, y + 6),
                    (cx + 34, base_y), (cx - 34, base_y)], (150, 160, 190))
    draw_rect_outline(img, cx - 34, y + 6, 68, base_y - y - 6, INK, 1)
    # window rows
    for wy in range(y + 16, base_y - 10, 12):
        half = 16 + (wy - y) // 6
        fill_rect(img, cx - half, wy, half * 2, 5, NAVY)
    # damage patch, mid-facade
    fill_poly(img, [(cx + 2, y + 34), (cx + 22, y + 40), (cx + 14, y + 56),
                    (cx + 24, y + 62), (cx + 4, y + 66), (cx - 2, y + 48)],
              DARK_GREY)
    # smoke wisp
    fill_circle(img, cx + 26, y + 28, 7, GREY)
    fill_circle(img, cx + 34, y + 18, 5, GREY)
    # small drone, top left
    dx, dy = x + 8, y + 12
    fill_rect(img, dx, dy, 16, 6, INK)
    draw_hline(img, dx - 6, dy - 3, 28, INK, 2)


def pic_scales(img, x, y, w, h):
    """Scales of justice with a guilty verdict count."""
    cx = x + w // 2
    top_y = y + 8
    base_y = y + h - 26
    # post and beam
    draw_vline(img, cx - 2, top_y + 6, base_y - top_y - 6, INK, 4)
    draw_hline(img, cx - 44, top_y, 88, INK, 4)
    fill_circle(img, cx, top_y, 5, GOLD)
    # pans
    for side in (-1, 1):
        px = cx + side * 44
        draw_line(img, px, top_y + 2, px - 16, top_y + 34, INK)
        draw_line(img, px, top_y + 2, px + 16, top_y + 34, INK)
        fill_triangle(img, px - 18, top_y + 34, px + 18, top_y + 34,
                      px, top_y + 52, GOLD)
    # base
    fill_rect(img, cx - 30, base_y, 60, 6, INK)
    draw_text_centered(img, cx, base_y + 10, "10 OF 12 COUNTS", 1, RED)


def pic_clinic(img, x, y, w, h):
    """Hospital with a red cross, evacuated in the Ebola zone."""
    bx, by = x + 14, y + 22
    bw, bh = w - 28, h - 30
    fill_rect(img, bx, by, bw, bh, (240, 240, 235))
    draw_rect_outline(img, bx, by, bw, bh, INK, 2)
    # red cross sign on the roof
    fill_rect(img, bx + bw // 2 - 14, by - 16, 28, 10, RED)
    fill_rect(img, bx + bw // 2 - 5, by - 25, 10, 28, RED)
    # windows and door
    for wx in range(bx + 10, bx + bw - 12, 26):
        fill_rect(img, wx, by + 10, 14, 12, LIGHT_BLUE)
        draw_rect_outline(img, wx, by + 10, 14, 12, INK, 1)
    fill_rect(img, bx + bw // 2 - 10, by + bh - 22, 20, 22, INK)
    # ambulance strip at the bottom
    ax = x + 8
    ay = y + h - 16
    fill_rect(img, ax, ay, 44, 12, (255, 255, 255))
    draw_rect_outline(img, ax, ay, 44, 12, RED, 2)
    fill_rect(img, ax + 18, ay + 3, 8, 3, RED)
    fill_rect(img, ax + 21, ay + 1, 3, 8, RED)
    fill_circle(img, ax + 10, ay + 13, 4, INK)
    fill_circle(img, ax + 34, ay + 13, 4, INK)


def pic_turkey(img, x, y, w, h):
    """A pardoned turkey with a fanned tail, on the White House lawn."""
    cx = x + w // 2
    gy = y + h - 8
    draw_hline(img, x + 4, gy, w - 8, GREEN, 4)
    # tail fan
    for ang, col in ((-52, BROWN), (-30, GOLD), (0, BROWN),
                     (30, GOLD), (52, BROWN)):
        tip_x = cx + int(46 * (ang / 52.0))
        tip_y = y + 12 + abs(ang) // 6
        fill_triangle(img, cx - 6, gy - 34, cx + 6, gy - 34,
                      tip_x, tip_y, col)
    # body
    fill_circle(img, cx, gy - 26, 20, BROWN)
    fill_circle(img, cx, gy - 22, 12, (150, 95, 40))
    # head and beak
    fill_circle(img, cx + 14, gy - 46, 9, BROWN)
    fill_triangle(img, cx + 22, gy - 48, cx + 32, gy - 44,
                  cx + 22, gy - 42, YELLOW)
    fill_circle(img, cx + 17, gy - 48, 2, INK)
    # wattle
    fill_rect(img, cx + 20, gy - 40, 4, 8, RED)
    # legs
    draw_vline(img, cx - 6, gy - 8, 8, YELLOW, 3)
    draw_vline(img, cx + 6, gy - 8, 8, YELLOW, 3)


# ------------------------------------------------------------------- layout
MARGIN = 32
CONTENT_W = W - 2 * MARGIN

STORIES = [
    ("ZELENSKIY: WE HIT RUSSIAN SHIP",
     "UKRAINE'S PRESIDENT CONFIRMS KYIV'S DRONE STRUCK THE RUSSIAN "
     "CARGO SHIP SPARTA II IN THE GULF OF FINLAND. HE SAYS IT "
     "CARRIED WEAPONS. NORWAY URGES CAUTION.",
     pic_ship_fire,
     "GULF OF FINLAND - EUROPE"),
    ("CIA AND ODNI HIT BY CYBERATTACK",
     "HACKERS BREACH UNCLASSIFIED SYSTEMS USED FOR OPEN SOURCE "
     "INTELLIGENCE, CNN REPORTS. NO CLASSIFIED DATA WAS HIT.",
     pic_cyber,
     ""),
    ("HOUTHI DRONE HITS RIYADH TOWER",
     "11 PEOPLE HURT AS A DRONE STRIKES RIYADH'S TALLEST TOWER, "
     "HOME TO THE SAUDI WEALTH FUND. SECOND HIT IN A WEEK.",
     pic_tower,
     ""),
    ("HUAWEI GUILTY IN US TRIAL",
     "A NEW YORK JURY FINDS THE CHINESE TECH GIANT GUILTY ON 10 "
     "OF 12 COUNTS, INCLUDING STEALING TRADE SECRETS.",
     pic_scales,
     ""),
    ("WHO STAFF FLEE CONGO HOSPITAL",
     "HEALTH WORKERS EVACUATED FROM A HOSPITAL IN AKWE, ITURI, "
     "AFTER THREE DAYS SHELTERING FROM FIERCE FIGHTING. THE EBOLA "
     "TEAM WAS ALSO MOVED.",
     pic_clinic,
     ""),
    ("TRUMP PARDONS TURKEYS FOR THANKSGIVING",
     "THE PRESIDENT SPARES TURKEYS FREEDOM AND FEATHERS AT THE "
     "WHITE HOUSE AHEAD OF THANKSGIVING. FEATHERS FIRST FLED INTO "
     "THE BUSHES.",
     pic_turkey,
     ""),
]


def draw_lead(img, story, y, height):
    headline, summary, pic, caption = story
    draw_text(img, MARGIN, y, headline, 4, INK)
    pic_y = y + 44
    pic_h = height - 54
    pic_w = 360
    draw_rect_outline(img, MARGIN, pic_y, pic_w, pic_h, INK, 2)
    pic(img, MARGIN + 2, pic_y + 2, pic_w - 4, pic_h - 4)
    tx = MARGIN + pic_w + 20
    tw = W - MARGIN - tx
    lines = wrap_text(summary, 2, tw)
    ly = pic_y + 6
    for line in lines:
        draw_text(img, tx, ly, line, 2, DARK_GREY)
        ly += 20
    draw_text(img, tx, pic_y + pic_h - 22, caption, 1, RED)
    return y + height


def draw_strip(img, story, y, height):
    headline, summary, pic, _caption = story
    pic_w = 150
    pic_h = height - 16
    draw_rect_outline(img, MARGIN, y + 8, pic_w, pic_h, INK, 2)
    pic(img, MARGIN + 2, y + 10, pic_w - 4, pic_h - 4)
    tx = MARGIN + pic_w + 18
    tw = W - MARGIN - tx
    draw_text(img, tx, y + 10, headline, 3, INK)
    lines = wrap_text(summary, 2, tw)
    ly = y + 40
    for line in lines[:3]:
        draw_text(img, tx, ly, line, 2, DARK_GREY)
        ly += 19
    return y + height


def main():
    img = new_image()
    # thin outer frame
    draw_rect_outline(img, 10, 10, W - 20, H - 20, INK, 3)

    # masthead
    draw_text_centered(img, W // 2, 30, "THE WORLD TODAY", 10, INK)
    draw_hline(img, MARGIN, 116, CONTENT_W, INK, 4)
    draw_text_centered(img, W // 2, 128, "WEDNESDAY, 25 NOVEMBER 2026", 2, RED)
    draw_hline(img, MARGIN, 152, CONTENT_W, INK, 2)
    draw_hline(img, MARGIN, 157, CONTENT_W, INK, 2)

    # lead story
    y = draw_lead(img, STORIES[0], 172, 252)
    draw_hline(img, MARGIN, y + 8, CONTENT_W, INK, 3)

    # five more stories as strips
    strip_y = y + 20
    strip_h = 102
    for story in STORIES[1:]:
        strip_y = draw_strip(img, story, strip_y, strip_h)
        draw_hline(img, MARGIN, strip_y - 2, CONTENT_W, GREY, 1)

    # footer
    draw_hline(img, MARGIN, 972, CONTENT_W, INK, 2)
    draw_text_centered(img, W // 2, 984,
                       "THE WORLD TODAY - WEDNESDAY 25 NOVEMBER 2026", 2, INK)

    out = "/output/entry.png" if os.path.isdir("/output") else "./entry.png"
    size = write_png(img, out)
    print("wrote %s (%d bytes)" % (out, size))


if __name__ == "__main__":
    main()
