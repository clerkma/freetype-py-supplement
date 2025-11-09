import freetype
from freetype.raw import FT_Load_Sfnt_Table
import ctypes
from struct import unpack_from

def load_sfnt_table(face: freetype.Face, tag):
    try:
        face_ref = face._FT_Face
        tag_u32 = ctypes.c_uint32(unpack_from(">L", tag.encode("U8"), 0)[0])
        len_i32 = ctypes.c_int32(0)
        FT_Load_Sfnt_Table(face_ref, tag_u32, 0, None, ctypes.byref(len_i32))
        if len_i32.value:
            buf_u8n = ctypes.create_string_buffer(len_i32.value)
            FT_Load_Sfnt_Table(face_ref, tag_u32, 0, buf_u8n, ctypes.byref(len_i32))
            return buf_u8n.raw
    except Exception as e:
        print(e)
