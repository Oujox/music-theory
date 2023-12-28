from abc import ABCMeta, abstractproperty
from .key import Key


class Scale(metaclass=ABCMeta):

    def __init__(self, key: str|Key):
        self.key = key if isinstance(key, Key) else Key(key)

    @property
    @abstractproperty
    def diatonic(self) -> list[Key]:
        pass
