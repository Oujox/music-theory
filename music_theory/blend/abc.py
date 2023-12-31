import typing as t
from abc import abstractmethod
from numpy import ndarray

from ..mstobject import MstMainObject


class BlendBase(MstMainObject):
    """
    """

    @abstractmethod
    def wave(self, sec: float) -> ndarray:
        pass

    @abstractmethod
    def play(self, sec: float) -> ndarray:
        pass

    @abstractmethod
    def save(self, path: str) -> str:
        pass
