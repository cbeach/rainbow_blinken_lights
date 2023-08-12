from dataclasses import dataclass
from enum import Enum
import colorsys
from typing import Callable, Tuple, Union

from rich.console import Console
from rich.color import Color as RichColor
from rich.segment import Segment
from rich.style import Style
from rich.color import Color as RichColor

from .named_colors import named_colors

class ColorSpace(Enum):
    RGB = 1
    HSV = 2

class MetaColor(type):
    def __getattr__(cls, item):
        if item in named_colors:
            return Color(_rgb=named_colors[item])
        else:
            raise AttributeError(f"'{cls.__class__.__name__}' object has no attribute '{item}'")

    def _overflow_behavior(cls, i) -> int:
        return cls._overflow_wrap(i)

    def _overflow_ciel(cls, i) -> int:
        return min(i, 255)

    def _overflow_wrap(cls, i) -> int:
        return i if i <= 255 else i - 255


@dataclass
class Color(metaclass=MetaColor):
    _red: int = None
    _green: int = None
    _blue: int = None
    _hue: int = None
    _saturation: int = None
    _value: int = None
    _r: int = None
    _g: int = None
    _b: int = None
    _h: int = None
    _s: int = None
    _v: int = None
    _rgb: Tuple[int, int, int] = None
    _hsv: Tuple[int, int, int] = None

    def __post_init__(self):
        self._console = Console()
        if self._red is not None and self._green is not None and self._blue is not None:
            self.rgb = (self._red, self._green, self._blue, )
        elif self._r is not None and self._g is not None and self._b is not None:
            self.rgb = (self._r, self._g, self._b, )
        elif self._hue is not None and self._saturation is not None and self._value is not None:
            self.hsv = (self._hue, self._saturation, self._value, )
        elif self._h is not None and self._s is not None and self._v is not None:
            self.hsv = (self._h, self._s, self._v, )
        elif self._rgb is not None:
            self.rgb = self._rgb
        elif self._hsv is not None:
            self.hsv = self._hsv
        else:
            raise ValueError('no color provided')

    def __getattr__(self, item):
        if item in named_colors:
            self.rgb = named_colors[item].rgb
            return self
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def __int__(self):
        return (self._r << 16) + (self._g << 8) + self._blue

    def __copy__(self):
        return Color(_rgb=self.rgb)

    def __deepcopy__(self, memodict={}):
        return Color(_rgb=self.rgb)

    @property
    def rgb(self):
        return self._rgb

    @property
    def red(self) -> int:
        return self._red

    @property
    def green(self) -> int:
        return self._green

    @property
    def blue(self) -> int:
        return self._blue

    @property
    def r(self) -> int:
        return self._r

    @property
    def g(self) -> int:
        return self._g

    @property
    def b(self) -> int:
        return self._b

    @property
    def hsv(self):
        return self._hsv

    @property
    def hue(self) -> int:
        return self._hue

    @property
    def saturation(self) -> int:
        return self._saturation

    @property
    def value(self) -> int:
        return self._value

    @property
    def h(self) -> int:
        return self._h

    @property
    def s(self) -> int:
        return self._s

    @property
    def v(self) -> int:
        return self._v

    def _from_int(self, value):
        self._blue = value & 255
        self._green = (value >> 8) & 255
        self._red = (value >> 16) & 255

    @rgb.setter
    def rgb(self, rgb: Union[Tuple[int, int, int], int]):
        if isinstance(rgb, int):
            self._from_int(rgb)
        else:
            self._red = self._r = Color._overflow_behavior(rgb[0])
            self._green = self._g = Color._overflow_behavior(rgb[1])
            self._blue = self._b = Color._overflow_behavior(rgb[2])
            self._rgb = (Color._overflow_behavior(rgb[0]), Color._overflow_behavior(rgb[1]), Color._overflow_behavior(rgb[2]) )
            h, s, v = colorsys.rgb_to_hsv(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0, )
            h, s, v = (int(h * 255), int(s * 255), int(v * 255), )
            self._hue = self._h = Color._overflow_behavior(h)
            self._saturation = self._s = Color._overflow_behavior(s)
            self._value = self._v = Color._overflow_behavior(v)
            self._hsv = (Color._overflow_behavior(h), Color._overflow_behavior(s), Color._overflow_behavior(v))

    @red.setter
    def red(self, r: int) -> None:
        self.rgb = (r, self._g, self._b)

    @green.setter
    def green(self, g: int) -> None:
        self.rgb = (self._r, g, self._b)

    @blue.setter
    def blue(self, b: int) -> None:
        self.rgb = (self._r, self._g, b)

    @r.setter
    def r(self, r: int) -> None:
        self.rgb = (r, self._g, self._b)

    @g.setter
    def g(self, g: int) -> None:
        self.rgb = (self._r, g, self._b)

    @b.setter
    def b(self, b: int) -> None:
        self._rgb = (self._r, self._g, b)

    @hsv.setter
    def hsv(self, hsv: Union[Tuple[int, int, int], int]) -> None:
        if isinstance(hsv, int):
            self._from_int(hsv)
        else:
            self._hue = self._h = Color._overflow_behavior(hsv[0])
            self._saturation = self._s = Color._overflow_behavior(hsv[1])
            self._value = self._v = Color._overflow_behavior(hsv[2])
            self._hsv = (Color._overflow_behavior(hsv[0]), Color._overflow_behavior(hsv[1]), Color._overflow_behavior(hsv[2]) )
            r, g, b = colorsys.hsv_to_rgb(hsv[0] / 255.0, hsv[1] / 255.0, hsv[2] / 255.0, )
            r, g, b = (int(r * 255), int(g * 255), int(b * 255), )
            self._red = self._r = Color._overflow_behavior(r)
            self._green = self._g = Color._overflow_behavior(g)
            self._blue = self._b = Color._overflow_behavior(b)
            self._rgb = (Color._overflow_behavior(r), Color._overflow_behavior(g), Color._overflow_behavior(b))

    @hue.setter
    def hue(self, h: int) -> None:
        self.hsv = (h, self._s, self._v)

    @saturation.setter
    def saturation(self, s: int) -> None:
        self.hsv = (self._h, s, self._v)

    @value.setter
    def value(self, v: int) -> None:
        self.hsv = (self._h, self._s, v)

    @h.setter
    def h(self, h: int) -> None:
        self.hsv = (h, self._s, self._v)

    @s.setter
    def s(self, s: int) -> None:
        self.hsv = (self._h, s, self._v)

    @v.setter
    def v(self, v: int) -> None:
        self.hsv = (self._h, self._s, v)

    def overflow(self, func: Callable[[int], int]) -> None:
        Color._overflow_behavior = func

    def show(self):
        bgcolor = RichColor.from_rgb(self._r, self._g, self._b)
        color = RichColor.from_rgb(self._r, self._g, self._b)
        return Segment("▄", Style(color=color, bgcolor=bgcolor))
