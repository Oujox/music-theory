
import typing as t
from .statics import NOON_QUALITIES


class _QualityCore:

    def __init__(self, quality: str, number: int):
        if not number in (qua := NOON_QUALITIES[quality]):
            self.__degree = (-12+number,)+qua
            self.__shift = 0
            self.__on = number
        else:
            self.__degree = qua
            self.__shift = number
            self.__on = 0

    @property
    def notes(self) -> int:
        return len(self.__degree)

    @property
    def degree(self) -> list[int]:
        i = self.__degree.index(self.__shift)
        q = self.__degree
        if self.isinvchord():
            q = q[i:] + tuple([ d+12 for d in q[:i] ])
            return [ j-self.__shift for j in q ]
        return [ j+(12-self.__on)%12 for j in q ]

    def __eq__(self, other: t.Self) -> bool:
        d = self.__degree == other.__degree
        s = self.__shift == other.__shift
        o = self.__on == other.__on
        return d & s & o

    def __ne__(self, other: t.Self) -> bool:
        return not self.__eq__(other)

    def inversion(self, rotate: int) -> None:
        if self.isonchord(): return
        shift = self.__degree[rotate%len(self.__degree)]
        self.__shift = shift

    def isonchord(self) -> bool:
        return bool(self.__on)

    def isinvchord(self) -> bool:
        return bool(self.__shift)


class Quality(_QualityCore):

    def __init__(self, quality: str, number: int):
        self._name = quality
        super().__init__(self.encode(quality), number)

    @property
    def quality(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self._name

    @classmethod
    def encode(cls, quality: str):
        return quality

    @classmethod
    def decode(cls, quality: str):
        return quality
