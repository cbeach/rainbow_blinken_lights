import random as rand
from typing import Any, Callable, Dict, List, Protocol

from .color import Color
from .strand import Strand

class AniInitFunc(Protocol):
    def __call__(self, i: int, strip: List[Color]) -> Color: ...

class AniTransFunc(Protocol):
    def __call__(self, i: int, strip: List[Color], init: bool = False) -> Color: ...

class Animations:
    class Initialization:
        @staticmethod
        def fill(color: Color = Color.black):
            def func(i: int, strip: List[Color]):
                return color
            return func

        @staticmethod
        def rainbow(i: int, strip: List[Color]):
            color = Color(_h=i, _s=255, _v=255)
            return color

        @staticmethod
        def first_pixel_to_color(color: Color):
            def init_func(i: int, strip: List[Color]):
                if i == 0:
                    return color
                else:
                    return Color.black
            return init_func

    class Transformation:
        @staticmethod
        def identity(pixel: Color):
            return pixel

        @staticmethod
        def cycle_hue(pixel: Color):
            return Color(pixel)

        @staticmethod
        def exponential_decay(decay_factor: float) -> Callable[[Color, int], Color]:
            def func(pixel: Color, t: int):
                r = int(pixel.r * decay_factor ** t)
                g = int(pixel.g * decay_factor ** t)
                b = int(pixel.b * decay_factor ** t)
                return Color(_rgb=(r, g, b))
            return func

        @staticmethod
        def rainbow(pixel: Color):
            h, s, v = pixel.h + 1 if pixel.h < 255 else 0, pixel.s, pixel.v
            return Color(_hsv=(h, s, v))
    @staticmethod
    def rainbow_cycle(i: int, strip: List[Color], init: bool = False) -> Color:
        if init is True:
            return Animations.Initialization.rainbow(i, strip)
        h, s, v = strip[i].hsv
        hp = h + 1 if h < 255 else 0
        color = Color(_hsv=(hp, s, v))
        return color

    @staticmethod
    def chase(init_func: AniInitFunc, transformation: AniTransFunc = Transformation.identity, step_length: int = 1, smooth: bool = False):
        def initialized_chase(i, strip, init=False):
            if init is True:
                return init_func(i, strip)
            if i + step_length >= len(strip):
                j = i + step_length - len(strip)
            else:
                j = i + step_length
            return transformation(strip[j])
        return initialized_chase

    @staticmethod
    def pixel_chase(color: Color = Color.white, transformation: AniTransFunc = Transformation.identity, step_length: int = 1, smooth: bool = False):
        def initialized_pixelChase(i, strip, init=False):
            if init is True:
                return Animations.Initialization.first_pixel_to_color(color)(i, strip)
            if i + step_length >= len(strip):
                j = i + step_length - len(strip)
            else:
                j = i + step_length
            return transformation(strip[j])
        return initialized_pixelChase

    @staticmethod
    def rainbow_chase(step_length: int = 1, smooth: bool = False):
        def initialized_pixelChase(i, strip, init=False):
            if init is True:
                return Animations.Initialization.first_pixel_to_color(Color(_hsv=(0, 255, 255)))(i, strip)
            if i + step_length >= len(strip):
                j = i + step_length - len(strip)
            else:
                j = i + step_length
            return Animations.Transformation.rainbow(strip[j])
        return initialized_pixelChase

    @staticmethod
    def multi_sparkle(strand_length: int, probability: float = .1, decay_rate: float = .95,
                pop: Callable[[int, List[Color], List[Dict[str, Any]]], Color] = lambda i, strip, state: Color.white):
        state = [dict(t=0) for i in range(strand_length)]
        decay_func = Animations.Transformation.exponential_decay(decay_rate)
        def func(i: int, strip: List[Color], init: bool = False) -> Color:
            if init is True:
                return Animations.Initialization.fill()(i, strip)
            if strip[i] == Color.black:
                if rand.random() < probability:
                    state[i]['t'] = 0
                    return pop(i, strip, state)
            else:
                state[i]['t'] += 1
                return decay_func(strip[i], state[i]['t'])
            return strip[i]
        return func

    @staticmethod
    def sparkle(strand_length: int, probability: float = .1, decay_rate: float = .95):
        return Animations.multi_sparkle(strand_length, probability, decay_rate)

    @staticmethod
    def rainbow_sparkle(strand_length: int, probability: float = .1, decay_rate: float = .95):
        def pop(i: int, strip: List[Color], state: List[Dict[str, Any]]) -> Color:
            return Color(_hsv=(rand.randint(0, 255), 255, 255))
        return Animations.multi_sparkle(strand_length, probability, decay_rate, pop=pop)
