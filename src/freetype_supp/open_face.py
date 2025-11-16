import freetype
import pathlib
import platform
import io
from PIL import Image
import numpy as np
from .enum import pixel_mode as ft_pixel_mode

def open_face(path: pathlib.Path, index=0):
    if path.exists():
        if platform.system() in ["Linux", "Darwin"]:
            return freetype.Face(path.as_posix(), index=index)
        else:
            data = io.BytesIO(path.read_bytes())
            return freetype.Face(data, index=index)

def get_image(face):
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
        return Image.fromarray(np.unpackbits(b).reshape((r, p * 8))[:, 0:w])
    elif m == ft_pixel_mode.GRAY:
        return Image.frombytes("L", (w, r), b)
    elif m == ft_pixel_mode.LCD or m == ft_pixel_mode.LCD_V:
        return Image.frombytes("RGB", (w, r), b)
    elif m == ft_pixel_mode.BGRA:
        image_bgra = np.frombuffer(b, dtype=np.uint8).reshape((-1, 4))
        image_rgba = image_bgra[..., (2, 1, 0, 3)].reshape((-1, w, 4))
        return Image.fromarray(image_rgba, "RGBA")
    # rare: GRAY2, GRAY4
