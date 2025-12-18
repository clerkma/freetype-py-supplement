import freetype
import pathlib
import platform
import io
from PIL import Image
import numpy as np
from .enum import pixel_mode as ft_pixel_mode
from .enum import render_mode

def open_face(path: pathlib.Path, index=0):
    if path.exists():
        if platform.system() in ["Linux", "Darwin"]:
            return freetype.Face(path.as_posix(), index=index)
        else:
            data = io.BytesIO(path.read_bytes())
            return freetype.Face(data, index=index)

def get_image(face, transform=lambda x: x):
    bmp = face.glyph.bitmap
    try:
        b = bytearray(bmp.buffer)
    except Exception as e:
        # maybe NULL
        print("get_image: fail to load bitmap", e)
        return
    w = bmp.width
    r = bmp.rows
    p = bmp.pitch
    if not (p * w):
        return
    m = ft_pixel_mode(bmp.pixel_mode)
    if m == ft_pixel_mode.MONO:
        data = 255 * np.unpackbits(b).reshape((r, p * 8))[:, 0:w]
        return Image.fromarray(transform(data), "L")
    elif m == ft_pixel_mode.GRAY:
        data = np.frombuffer(b, dtype=np.uint8).reshape((-1, p))[:, 0:w]
        return Image.fromarray(transform(data), "L")
    elif m == ft_pixel_mode.LCD or m == ft_pixel_mode.LCD_V:
        data = np.frombuffer(b, dtype=np.uint8).reshape((-1, p))[:, 0:w].reshape((-1, w // 3, 3))
        return Image.fromarray(transform(data), "RGB")
    elif m == ft_pixel_mode.BGRA:
        image_bgra = np.frombuffer(b, dtype=np.uint8).reshape((-1, 4))
        data = image_bgra[..., (2, 1, 0, 3)].reshape((-1, w, 4))
        return Image.fromarray(transform(data), "RGBA")
    # rare: GRAY2, GRAY4

class glyph_bitmap:
    def __init__(self, face):
        self.image = get_image(face, lambda x: 255 - x)
        self.left = face.glyph.bitmap_left
        self.top = face.glyph.bitmap_top
        self.adv = face.glyph.advance.x >> 6
        self.bot = self.image.height - self.top

    def __str__(self):
        return (
            f"left={self.left:3},"
            f"top={self.top:4},"
            f"adv={self.adv:4},"
            f"bot={self.bot:4},"
            f"img={self.image.size}"
        )

def draw_text_simplex(
        face: freetype.Face, text: str,
        mode: render_mode=render_mode.LIGHT,
        margin: tuple=(1, 1, 1, 1)):
    glyph_list = []
    h = 0
    d = 0
    w = 0
    for char in text:
        face.load_char(char, 0)
        face.glyph.render(mode.value)
        glyph = glyph_bitmap(face)
        glyph_list.append(glyph)
        h = max(h, glyph.top)
        d = max(d, glyph.bot)
        w += glyph.left + glyph.adv
    if not glyph_list:
        return
    mode = glyph_list[0].image.mode
    image_w = w + margin[0] + margin[1]
    image_h = h + d + margin[2] + margin[3]
    image = Image.new(mode, (image_w, image_h), 0xFFFFFFFF)
    x = margin[0]
    y = margin[2] + h
    for glyph in glyph_list:
        x0 = x + glyph.left
        x1 = x0 + glyph.image.width
        y0 = y - glyph.top
        y1 = y + glyph.bot
        image.paste(glyph.image, (x0, y0, x1, y1))
        x += glyph.left + glyph.adv
    return image