import freetype
from freetype.raw import FT_Get_TrueType_Engine_Type
from .enum import truetype_engine_type

def get_truetype_engine_type():
    value = int(FT_Get_TrueType_Engine_Type(freetype._handle))
    if 0 <= value <= 2:
        return truetype_engine_type(value)
