import time
from copy import deepcopy
import signal
import sys
from threading import Event
from time import sleep
from typing import List, Protocol, Tuple, Union, Iterable

import sh

from .color import Color, ColorSpace
from sh import grep
MOCK = False
try:
    grep('-i', 'raspbian', '/etc/os-release').lower()
    from rpi_ws281x import PixelStrip
except sh.ErrorReturnCode as ex:
    MOCK = True
    from .mock_pixel_strip import PixelStrip

TColor = Union[Tuple[int, int, int], Color]
class TransitionFunction(Protocol):
    def __call__(self, i, pixels: List[Color], init: bool = False) -> Color: ...

class Strand:
    _func = None
    def __init__(self, led_count: int, pin: int = 18, frequency: int = 800000, dma: int = 10, invert: bool = False,
                 max_brightness: int = 255, channel: int = 0, delay_ms: float = 50):
        """
        LED_COUNT = 16  # Number of LED pixels.
        LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
        # LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10  # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
        """
        self._exitEvent = Event()
        def keyboard_interupt(signo, _frame):
            print("Clearing strip. Exiting.")
            self._exitEvent.set()

        for sig in ('TERM', 'HUP', 'INT'):
            signal.signal(getattr(signal, 'SIG' + sig), keyboard_interupt);

        self._strip = PixelStrip(led_count, pin, frequency, dma, invert, max_brightness, channel)
        self._strip.begin()
        self._pixels = [Color(0, 0, 0) for _ in range(led_count)]
        self._delay = delay_ms / 1000.0
        def identity(i, pixels, init=False):
            return pixels[i]

        self.transition_function = identity


    def __len__(self):
        return len(self._pixels)

    @property
    def transition_function(self) -> TransitionFunction:
        return self._func

    @transition_function.setter
    def transition_function(self, func: TransitionFunction):
        self._func = func
        self._step(init=True)

    def _main(self):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.clear()

    def setPixelColor(self, n, color):
        self._pixels[n] = color
        self._strip.setPixelColorRGB(n, color.r, color.b, color.g)

    def _lock(self, pixels: List[Color] = []):
        if len(pixels) == len(self._pixels):
            self._pixels = pixels

        for i, pixel in enumerate(self._pixels):
            self.setPixelColor(i, pixel)
        self._strip.show()

    def _convert_color(self, _color: TColor, color_space: ColorSpace = ColorSpace.RGB) -> Color:
        try:
            iter(_color)
            if len(_color) == 3:
                if color_space == ColorSpace.RGB:
                    return Color(_rgb=_color)
                elif color_space == ColorSpace.HSV:
                    return Color(_hsv=_color)
                else:
                    raise ValueError(f'Invalid color: _convert_color({_color=}, {color_space=})')
            else:
                raise ValueError(f'Invalid color: _convert_color({_color=}, {color_space=})')
        except TypeError as te:
            # _color is not iterable
            pass

        if isinstance(_color, Color):
            return _color
        else:
            raise ValueError(f'Invalid color: _convert_color({_color=}, {color_space=})')

        #match _color:
        #    case (a, b, c):
        #        match color_space:
        #            case ColorSpace.RGB:
        #                color = (a, b, c)
        #            case ColorSpace.HSV:
        #                color = Color(_h=a, _s=b, _v=c).rgb
        #            case _:
        #                raise ValueError(f'Invalid color: _convert_color({_color=}, {color_space=})')
        #    case Color():
        #        color = _color.rgb
        #    case _:
        #        raise ValueError(f'Invalid color: _convert_color({_color=}, {color_space=})')

    def fill(self, _color: TColor, color_space: ColorSpace = ColorSpace.RGB, quick=False):
        color = self._convert_color(_color, color_space)
        for i, _ in enumerate(self._pixels):
            self.setPixelColor(i, color)
            if quick is False:
                self._exitEvent.wait(self._delay)
                self._lock()
        self._lock()

    def _step(self, init=False):
        self._lock(
            [self.transition_function(i, self._pixels, init=init) for i in range(len(self._pixels))]
        )

    def loop(self, iterations=None):
        while not self._exitEvent.is_set() and (iterations is None or iterations == 0):
            if iterations is not None:
                iterations -= 1
            self.show()
            self._exitEvent.wait(self._delay)
        self.clear()

    def show(self, step=True, end='\r'):
        if step is True:
            self._step()
        if MOCK is True:
            self._strip.show(end=end)
        else:
            self._strip.show()

    def clear(self):
        self.fill(Color.black, quick=True)
        self._lock()

