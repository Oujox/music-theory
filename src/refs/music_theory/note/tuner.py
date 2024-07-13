
import functools
import typing as t
from .abstract import BaseTuner, BaseScale


class EqualTemperament:

    equal: t.Final[int]

    def __init_subclass__(cls, /, equal: int, **kwargs) -> None:
        cls.equal: int = equal
        return super().__init_subclass__(**kwargs)

class UnequalTemperament:
    ...


def compress_ratio(ratio: float) -> float:
        while ratio > 2:
            ratio = ratio / 2
        while ratio < 1:
            ratio = ratio * 2
        return ratio

def  standard_tuning_table(p5th_ratio: float) -> tuple[float]:
    # https://en.wikipedia.org/wiki/Just_intonation#Five-limit_tuning
    (ratios := [
        compress_ratio(p5th_ratio ** i)
        for i in range(12)
    ]).sort()

    return tuple(ratios)

pythagorean_tuning_table = functools.partial(standard_tuning_table, 1.5)
meantone_tuning_table = functools.partial(standard_tuning_table, (5 ** 0.25))


def  fivelimit_tuning_table() -> tuple[float]:
    # https://en.wikipedia.org/wiki/Just_intonation#Five-limit_tuning
    (ratios := [
        compress_ratio((3**j) * (5**i))
        for i in range(-1, 1+1)
        for j in range(-2, 2+1)
        if not j == -2
    ]).sort()

    return tuple(ratios)






class JustIntonationTuner(UnequalTemperament, BaseTuner):

    ratios : t.Final[tuple[float]] = fivelimit_tuning_table()

    def __init__(self, root: float, scale: BaseScale) -> None:
        self.root  = root
        self.scale = scale

    def hz(self, note_number: int) -> float:
        relative_number = note_number-69
        return self.root*(note_number-69)


class MeantoneTuner(UnequalTemperament, BaseTuner):

    ratios : t.Final[tuple[int]] = meantone_tuning_table()

    def __init__(self, root: float, scale: BaseScale) -> None:
        self.root  = root
        self.scale = scale

    def hz(self, note_number: int) -> float:
        return self.root*(note_number-69)


class PythagoreanTuner(UnequalTemperament, BaseTuner):

    def __init__(self, root: float, scale: BaseScale) -> None:
        self.root  = root
        self.scale = scale

    def hz(self, note_number: int) -> float:
        return self.root*(note_number-69)


class Equal12Tuner(EqualTemperament, BaseTuner, equal=12):

    def __init__(self, root: float) -> None:
        self.root = root

    def hz(self, note_number: int) -> float:
        return self.root*2**((note_number-69)/self.equal)

