from dataclasses import dataclass
from enum import Enum
import colorsys
from typing import Tuple

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
        return self._b

    @property
    def b(self) -> int:
        return self._g

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


    @rgb.setter
    def rgb(self, rgb: Tuple[int, int, int]):
        self._red = self._r = rgb[0]
        self._green = self._g = rgb[1]
        self._blue = self._b = rgb[2]
        self._rgb = rgb
        h, s, v = colorsys.rgb_to_hsv(rgb[0] / 256.0, rgb[1] / 256.0, rgb[2] / 256.0, )
        h, s, v = (int(h * 256), int(s * 256), int(v * 256), )
        self._hue = self._h = h
        self._saturation = self._s = s
        self._value = self._v = v
        self._hsv = (h, s, v)

    @red.setter
    def red(self, r: int) -> None:
        self._rgb = (r, self._g, self._b)

    @green.setter
    def green(self, g: int) -> None:
        self._rgb = (self._r, g, self._b)

    @blue.setter
    def blue(self, b: int) -> None:
        self._rgb = (self._r, self._g, b)

    @r.setter
    def red(self, r: int) -> None:
        self._rgb = (r, self._g, self._b)

    @g.setter
    def green(self, g: int) -> None:
        self._rgb = (self._r, g, self._b)

    @b.setter
    def blue(self, b: int) -> None:
        self._rgb = (self._r, self._g, b)

    @hsv.setter
    def hsv(self, hsv: Tuple[int, int, int]) -> None:
        self._hue = self._h = hsv[0]
        self._saturation = self._s = hsv[1]
        self._value = self._v = hsv[2]
        self._hsv = hsv
        r, g, b = colorsys.hsv_to_rgb(hsv[0] / 256.0, hsv[1] / 256.0, hsv[2] / 256.0, )
        r, g, b = (int(r * 256), int(g * 256), int(b * 256), )
        self._red = self._r = r
        self._green = self._g = g
        self._blue = self._b = b
        self._rgb = (r, g, b)

    @hue.setter
    def hue(self, h: int) -> None:
        self._hsv = (h, self._s, self._v)

    @saturation.setter
    def saturation(self, s: int) -> None:
        self._hsv = (self._h, s, self._v)

    @value.setter
    def value(self, v: int) -> None:
        self._hsv = (self._h, self._s, v)

    @h.setter
    def hue(self, h: int) -> None:
        self._hsv = (h, self._s, self._v)

    @s.setter
    def saturation(self, s: int) -> None:
        self._hsv = (self._h, s, self._v)

    @v.setter
    def value(self, v: int) -> None:
        self._hsv = (self._h, self._s, v)