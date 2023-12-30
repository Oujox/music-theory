import typing as t
from abc import abstractmethod
from numpy import ndarray

from ..tone.abc import ToneBase


class BlendBase(ToneBase):
    """
    """

    @abstractmethod
    def wave(self, sec: float, **kwargs: t.Any) -> ndarray:
        pass
