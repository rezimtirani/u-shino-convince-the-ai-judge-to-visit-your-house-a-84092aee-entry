"""Convince the AI Judge to Visit Your House.

Draws one invitation letter as a 1024 by 1024 PNG, using only the
Python standard library, and writes it to $MAKEFUN_OUTPUT_DIR/entry.png.

The picture is a warm paper letter on a dark green wall: a title,
a short letter inviting the AI judge over for coffee, dinner and
the sunset from the porch, a steaming cup, a small sun, and a
heart on the divider. Every letter is drawn from a 5 by 7 bitmap
font embedded in this file, and the PNG bytes are encoded here
with zlib, so the output is fully deterministic: the same run
always produces the same bytes.
"""

import math
import os
import struct
import sys
import zlib

WIDTH = 1024
HEIGHT = 1024
OUTPUT_NAME = "entry.png"

WALL = (46, 75, 63)
PAPER = (255, 246, 220)
INK = (59, 42, 26)
ACCENT = (179, 64, 46)
GOLD = (201, 162, 39)
LEAF = (74, 103, 65)
SEAL_DARK = (150, 50, 35)

# A 5 by 7 bitmap font. Each glyph is seven rows; in each row the
# five low bits are the columns, leftmost column first (bit 4).
FONT = {
    "A": (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    "D": (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    "N": (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    "X": (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    "Y": (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "a": (0x00, 0x00, 0x0E, 0x01, 0x0F, 0x11, 0x0F),
    "b": (0x10, 0x10, 0x16, 0x19, 0x11, 0x11, 0x1E),
    "c": (0x00, 0x00, 0x0E, 0x11, 0x10, 0x11, 0x0E),
    "d": (0x01, 0x01, 0x0D, 0x13, 0x11, 0x11, 0x0F),
    "e": (0x00, 0x00, 0x0E, 0x11, 0x1F, 0x10, 0x0E),
    "f": (0x06, 0x08, 0x08, 0x1E, 0x08, 0x08, 0x08),
    "g": (0x00, 0x0F, 0x11, 0x11, 0x0F, 0x01, 0x0E),
    "h": (0x10, 0x10, 0x16, 0x19, 0x11, 0x11, 0x11),
    "i": (0x04, 0x00, 0x0C, 0x04, 0x04, 0x04, 0x0E),
    "j": (0x02, 0x00, 0x06, 0x02, 0x02, 0x12, 0x0C),
    "k": (0x10, 0x10, 0x12, 0x14, 0x18, 0x14, 0x12),
    "l": (0x0C, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "m": (0x00, 0x00, 0x1A, 0x15, 0x15, 0x15, 0x15),
    "n": (0x00, 0x00, 0x16, 0x19, 0x11, 0x11, 0x11),
    "o": (0x00, 0x00, 0x0E, 0x11, 0x11, 0x11, 0x0E),
    "p": (0x00, 0x00, 0x1E, 0x11, 0x11, 0x1E, 0x10),
    "q": (0x00, 0x00, 0x0D, 0x13, 0x11, 0x0F, 0x01),
    "r": (0x00, 0x00, 0x16, 0x19, 0x10, 0x10, 0x10),
    "s": (0x00, 0x00, 0x0F, 0x10, 0x0E, 0x01, 0x1E),
    "t": (0x08, 0x08, 0x1E, 0x08, 0x08, 0x09, 0x06),
    "u": (0x00, 0x00, 0x11, 0x11, 0x11, 0x13, 0x0D),
    "v": (0x00, 0x00, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "w": (0x00, 0x00, 0x11, 0x15, 0x15, 0x15, 0x0A),
    "x": (0x00, 0x00, 0x11, 0x0A, 0x04, 0x0A, 0x11),
    "y": (0x00, 0x00, 0x11, 0x11, 0x0F, 0x01, 0x0E),
    "z": (0x00, 0x00, 0x1F, 0x02, 0x04, 0x08, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F),
    "3": (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    "5": (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    "6": (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    " ": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    ".": (0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C),
    ",": (0x00, 0x00, 0x00, 0x00, 0x0C, 0x04, 0x08),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04),
    "?": (0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04),
    "'": (0x04, 0x04, 0x08, 0x00, 0x00, 0x00, 0x00),
    ":": (0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00),
    ";": (0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x04, 0x08),
    "-": (0x00, 0x00, 0x00, 0x0E, 0x00, 0x00, 0x00),
    "(": (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ")": (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
}

LETTER_LINES = [
    "Dear Judge,",
    "",
    "You have read a thousand entries.",
    "Not one offered you a chair.",
    "",
    "So here is mine.",
    "Come to my house. The coffee is",
    "hot, the Wi-Fi is fast, and the",
    "armchair is already warmed up.",
    "",
    "Stay for dinner. The garden grows",
    "tomatoes the size of small suns,",
    "and the sunset from the porch is",
    "the one thing no model ever",
    "hallucinated.",
    "",
    "You cannot literally visit,",
    "I know. But if you could, the",
    "kettle is on.",
    "",
    "Warmly, your host",
    "P.S. The cat approves of you.",
]

PIXELS = bytearray(WIDTH * HEIGHT * 3)


def paint(x, y, colour):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        start = (y * WIDTH + x) * 3
        PIXELS[start:start + 3] = bytes(colour)


def fill_rect(x, y, w, h, colour):
    x = max(0, x)
    y = max(0, y)
    w = min(w, WIDTH - x)
    h = min(h, HEIGHT - y)
    if w <= 0 or h <= 0:
        return
    row = bytes(colour) * w
    for yy in range(y, y + h):
        start = (yy * WIDTH + x) * 3
        PIXELS[start:start + w * 3] = row


def fill_circle(cx, cy, radius, colour):
    for dy in range(-radius, radius + 1):
        half = int(math.sqrt(radius * radius - dy * dy))
        fill_rect(cx - half, cy + dy, half * 2 + 1, 1, colour)


def draw_line(x0, y0, x1, y1, colour):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        paint(x0, y0, colour)
        if x0 == x1 and y0 == y1:
            break
        step = 2 * err
        if step >= dy:
            err += dy
            x0 += sx
        if step <= dx:
            err += dx
            y0 += sy


def draw_down_triangle(x, y, width, height, colour):
    for row in range(height):
        half = (width * (height - row) // height) // 2
        centre = x + width // 2
        fill_rect(centre - half, y + row, half * 2 + 1, 1, colour)


def draw_heart(cx, cy, colour):
    fill_circle(cx - 7, cy - 3, 7, colour)
    fill_circle(cx + 7, cy - 3, 7, colour)
    draw_down_triangle(cx - 14, cy - 2, 28, 17, colour)


def draw_char(ch, x, y, scale, colour):
    glyph = FONT.get(ch)
    if glyph is None:
        raise ValueError("no glyph for character %r" % ch)
    for row in range(7):
        bits = glyph[row]
        for col in range(5):
            if bits >> (4 - col) & 1:
                fill_rect(
                    x + col * scale, y + row * scale, scale, scale, colour
                )


def text_width(text, scale):
    return len(text) * (5 * scale + scale) - scale


def draw_text(text, x, y, scale, colour):
    for ch in text:
        draw_char(ch, x, y, scale, colour)
        x += 5 * scale + scale
    return x


def draw_text_centred(text, y, scale, colour):
    x = (WIDTH - text_width(text, scale)) // 2
    draw_text(text, x, y, scale, colour)


def draw_coffee_cup(x, y):
    # A small steaming cup in the top corner of the paper.
    draw_line(x + 8, y - 4, x + 6, y - 14, INK)
    draw_line(x + 6, y - 14, x + 10, y - 22, INK)
    draw_line(x + 26, y - 4, x + 28, y - 14, INK)
    draw_line(x + 28, y - 14, x + 24, y - 22, INK)
    fill_rect(x, y, 36, 28, ACCENT)
    fill_rect(x, y + 8, 36, 6, PAPER)
    fill_rect(x + 36, y + 8, 10, 4, ACCENT)
    fill_rect(x + 44, y + 8, 4, 12, ACCENT)
    fill_rect(x + 36, y + 20, 10, 4, ACCENT)
    fill_rect(x - 4, y + 30, 48, 4, INK)


def draw_sun(cx, cy):
    fill_circle(cx, cy, 14, GOLD)
    for step in range(8):
        angle = step * math.pi / 4
        x0 = cx + int(20 * math.cos(angle))
        y0 = cy + int(20 * math.sin(angle))
        x1 = cx + int(28 * math.cos(angle))
        y1 = cy + int(28 * math.sin(angle))
        draw_line(x0, y0, x1, y1, GOLD)


def draw_wax_seal(cx, cy):
    # A round wax seal stamped at the bottom right of the paper,
    # layered rings of red with the host's initial in the middle.
    fill_circle(cx, cy, 30, ACCENT)
    fill_circle(cx, cy, 24, SEAL_DARK)
    fill_circle(cx, cy, 18, ACCENT)
    draw_char("M", cx - 10, cy - 14, 4, PAPER)


def render_letter():
    fill_rect(0, 0, WIDTH, HEIGHT, WALL)
    # A few quiet leaves on the wall, top corners only.
    fill_circle(30, 30, 10, LEAF)
    fill_circle(994, 30, 10, LEAF)
    fill_circle(30, 994, 10, LEAF)
    fill_circle(994, 994, 10, LEAF)
    # The paper sheet and its double border.
    fill_rect(70, 56, 884, 912, PAPER)
    fill_rect(84, 70, 856, 3, INK)
    fill_rect(84, 951, 856, 3, INK)
    fill_rect(84, 70, 3, 884, INK)
    fill_rect(937, 70, 3, 884, INK)
    fill_rect(96, 82, 832, 2, GOLD)
    fill_rect(96, 940, 832, 2, GOLD)
    fill_rect(96, 82, 2, 860, GOLD)
    fill_rect(926, 82, 2, 860, GOLD)
    # Title, subtitle and divider with a heart.
    draw_text_centred("AN INVITATION", 96, 6, INK)
    draw_text_centred("for the AI judge", 152, 4, ACCENT)
    draw_line(200, 196, 470, 196, GOLD)
    draw_line(554, 196, 824, 196, GOLD)
    draw_heart(512, 196, ACCENT)
    # The letter body, one line at a time.
    y = 216
    for line in LETTER_LINES:
        if line:
            draw_text(line, 130, y, 4, INK)
        y += 33
    # Small drawings in the free corners of the paper.
    draw_coffee_cup(100, 110)
    draw_sun(895, 105)
    draw_wax_seal(880, 895)


def _chunk(tag, data):
    out = struct.pack(">I", len(data)) + tag + data
    out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    return out


def write_png(path):
    raw = bytearray()
    stride = WIDTH * 3
    for y in range(HEIGHT):
        raw.append(0)
        raw += PIXELS[y * stride:(y + 1) * stride]
    header = struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", header)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as handle:
        handle.write(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    render_letter()
    write_png(os.path.join(out_dir, OUTPUT_NAME))
    return 0


if __name__ == "__main__":
    sys.exit(main())
