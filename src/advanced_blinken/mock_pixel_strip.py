import sys
from rich.segment import Segment
from rich.color import Color as RichColor
from rich.console import Console, ConsoleOptions, RenderResult
from .color import Color

class PixelStrip:
    def __init__(self, num, pin, freq_hz=800000, dma=10, invert=False,
                 brightness=255, channel=0, strip_type=None, gamma=None):
        self._leds = [Color(0, 0, 0) for i in range(num)]
        self._console = Console()

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        for pix in self._leds:
            yield pix.show()

    def __getitem__(self, pos):
        """Return the 24-bit RGB color value at the provided position or slice
        of positions.
        """
        return int(self._leds[pos])

    def __setitem__(self, pos, value):
        """Set the 24-bit RGB color value at the provided position or slice of
        positions.
        """
        self._leds[pos].rgb = value

    def __len__(self):
        return len(self._leds)

    def _cleanup(self):
        pass

    def setGamma(self, gamma):
        return 0

    def begin(self):
        """Initialize library, must be called once before other functions are
        called.
        """
        pass

    def show(self, end='\r'):
        """Update the display with the data from the LED buffer."""
        with self._console.capture() as capture:
            self._console.print(self, end=end)
        print(capture.get(), end=end)

    def setPixelColor(self, n, color):
        """Set LED at position n to the provided 24-bit color value (in RGB order).
        """
        self[n] = color

    def setPixelColorRGB(self, n, red, green, blue, white=0):
        """Set LED at position n to the provided red, green, and blue color.
        Each color component should be a value from 0 to 255 (where 0 is the
        lowest intensity and 255 is the highest intensity).
        """
        #print("\tsetPixelColorRGB1", self._leds[n].hsv)
        self._leds[n] = Color(_r=red, _g=green, _b=blue)
        #print("\tsetPixelColorRGB2", self._leds[n].hsv)

    def getBrightness(self):
        return 255

    def setBrightness(self, brightness):
        """Scale each LED in the buffer by the provided brightness.  A brightness
        of 0 is the darkest and 255 is the brightest.
        """
        pass

    def getPixels(self):
        """Return an object which allows access to the LED display data as if
        it were a sequence of 24-bit RGB values.
        """
        return [int(i) for i in self._leds]

    def numPixels(self):
        """Return the number of pixels in the display."""
        return len(self._leds)

    def getPixelColor(self, n):
        """Get the 24-bit RGB color value for the LED at position n."""
        return int(self[n])

    def getPixelColorRGB(self, n):
        return self._leds[n].rgb

    def getPixelColorRGBW(self, n):
        return self._leds[n].rgb
