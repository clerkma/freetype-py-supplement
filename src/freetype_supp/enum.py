from enum import Enum

class kening_mode(Enum):
    DEFAULT = 0
    UNFITTED = 1
    UNSCALED = 2

class lcd_filter(Enum):
    NONE = 0
    DEFAULT = 1
    LIGHT = 2
    LEGACY1 = 3
    LEGACY = 16
    MAX = 17

class load_flags(Enum):
    DEFAULT = 0
    NO_SCALE = (1 << 0)
    NO_HINTING = (1 << 1)
    RENDER = (1 << 2)
    NO_BITMAP = (1 << 3)
    VERTICAL_LAYOUT = (1 << 4)
    FORCE_AUTOHINT = (1 << 5)
    CROP_BITMAP = (1 << 6)
    PEDANTIC = (1 << 7)
    IGNORE_GLOBAL_ADVANCE_WIDTH = (1 << 9)
    NO_RECURSE = (1 << 10)
    IGNORE_TRANSFORM = (1 << 11)
    MONOCHROME = (1 << 12)
    LINEAR_DESIGN = (1 << 13)
    SBITS_ONLY = (1 << 14)
    NO_AUTOHINT = (1 << 15)
    COLOR = (1 << 20)
    COMPUTE_METRICS = (1 << 21)
    BITMAP_METRICS_ONLY = (1 << 22)
    NO_SVG = (1 << 24)

class truetype_engine_type(Enum):
    NONE = 0
    UNPATENTED = 1
    PATENTED = 2

class pixel_mode(Enum):
    NONE = 0
    MONO = 1
    GRAY = 2
    GRAY2 = 3
    GRAY4 = 4
    LCD = 5
    LCD_V = 6
    BGRA = 7
    MAX = 8

class render_mode(Enum):
    NORMAL = 0
    LIGHT = 1
    MONO = 2
    LCD = 3
    LCD_V = 4
    SDF = 5
    MAX = 6
