
import typing as t
from .abstract import BaseNote
from ._statics import NOTENAME_TO_PITCH, PITCH_TO_NOTENAME, ALL_KEYNAME, FIFTH_SEQUENCE


class Key(BaseNote):

    def __init__(self, name: str) -> None:

        if not self.is_keyname(name):
            raise ValueError()

        self._name  = name
        self._pitchclass = NOTENAME_TO_PITCH[name]

        self._fifth = FIFTH_SEQUENCE.index(self._pitchclass)
        self._accsidental: int = PITCH_TO_NOTENAME[self._pitchclass].index(self._name) - 2

    @property
    def name(self) -> str:
        return self._name

    @property
    def pitchclass(self) -> int:
        return self._pitchclass

    @property
    def fifth(self) -> int:
        return self._fifth

    @property
    def accsidental(self) -> int:
        return self._accsidental

    def __int__(self) -> int:
        return self._fifth

    def __str__(self) -> str:
        return "<Key: {}>".format(self._name)

    def __repr__(self) -> str:
        return "<Key: {}>".format(self._name)

    @classmethod
    def is_keyname(cls, name: str) -> t.TypeGuard[str]:
        return isinstance(name, str) and name in ALL_KEYNAME
