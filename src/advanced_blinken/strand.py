from time import sleep
from typing import Callable, List, Tuple, Union, Iterable
from rpi_ws281x import PixelStrip
from .color import Color, ColorSpace

TColor = Union[Tuple[int, int, int], Color]
TransitionFunction = Callable[[int, List[Color]], None]


class Strand: #(PixelStrip):
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
        #super(Strand, self).__init__(led_count, pin, frequency, dma, invert, max_brightness, channel)
        self._pixels = [Color(0, 0, 0) for _ in range(led_count)]
        self._delay = delay_ms / 1000.0
        #self.begin()

    @property
    def transition_function(self, func: TransitionFunction):
        self._func = func

    @transition_function.getter
    def transition_function(self) -> TransitionFunction:
        if self._func is None:
            return NotImplemented
        return self._func

    def _main(self):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.clear()

    def setPixelColor(self, n, color):
        pass

    def _lock(self):
        for i, pixel in enumerate(self._pixels):
            self.setPixelColor(i, pixel.rgb)

    def _convert_color(self, _color: TColor, color_space: ColorSpace = ColorSpace.RGB):
        match _color:
            case (a, b, c):
                match color_space:
                    case ColorSpace.RGB:
                        color = (a, b, c)
                    case ColorSpace.HSV:
                        color = Color(_h=a, _s=b, _v=c).rgb
                    case _:
                        raise ValueError(f'Invalid color: _convert_color({_color=}, {color_space=})')
            case Color():
                color = _color.rgb
            case _:
                raise ValueError(f'Invalid color: _convert_color({_color=}, {color_space=})')

        return color

    def fill(self, _color: TColor, color_space: ColorSpace = ColorSpace.RGB, quick=False):
        color = self._convert_color(_color, color_space)
        for pixel in self._pixels:
            pixel.rgb = color
            if quick is False:
                sleep(self._delay)

    def clear(self):
        self.fill()
        self._lock()

