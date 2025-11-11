import freetype
import pathlib
import platform
import io

def open_face(path: pathlib.Path, index=0):
    if path.exists():
        if platform.system() in ["Linux", "Darwin"]:
            return freetype.Face(path.as_posix(), index=index)
        else:
            data = io.BytesIO(path.read_bytes())
            return freetype.Face(data, index=index)
