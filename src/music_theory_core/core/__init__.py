
import typing as t

import string
import functools as f

from .base import ObjectMT

PRESENTATION_LANGUAGE = "ja"
PRESENTATION_SEMITONES = 12


class StaticMT(ObjectMT, st=PRESENTATION_SEMITONES):
    """
    """
    # NOTE: deprecated class property: https://github.com/python/cpython/issues/89519

    @property
    @f.lru_cache(maxsize=1)
    def notename(cls) -> tuple[str]:
        return tuple(string.ascii_uppercase[:cls.SEMITONES])

    @property
    @f.lru_cache(maxsize=1)
    def pitchclass(self) -> tuple[int]:
        return

    @f.lru_cache(maxsize=1)
    def to_notename(self, pitchclass: int) -> str:
        return

    @f.lru_cache(maxsize=1)
    def to_pitchclass(self, notename: str) -> int:
        return


class CoreMT(ObjectMT):
    """
    """

    PRESENTATION: t.Final[StaticMT]

    def __init_subclass__(cls, /, st: int, **kwargs) -> None:
        cls.PRESENTATION = StaticMT()
        super().__init_subclass__(st, **kwargs)

