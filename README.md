# Supplement to `freetype-py`

some missing functions or utils.

Functions:
* `get_truetype_engine_type()`
* `load_sfnt_table(face: Face, tag: str)`

Utils:
* `open_face(path: pathlib.Path, index: int)`
* `get_image(face: Face, transform=lambda x: x)`
* `draw_text_simplex(face: Face, text: str, mode: render_mode, margin: tuple)`
