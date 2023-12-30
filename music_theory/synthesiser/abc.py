import typing as t
from abc import ABCMeta, abstractmethod
from numpy import ndarray

from ..mst_object import MstSubObject


class OscillatorBase(metaclass=ABCMeta):

    def __init__(self, sampling_hz: int = 44100) -> None:
        self.sampling_hz = sampling_hz

    @abstractmethod
    def wave(self, hz: float, sec: float) -> ndarray:
        pass


class FilterBase(metaclass=ABCMeta):
    pass


class EnvelopeBase(metaclass=ABCMeta):
    pass


class ModulatorBase(metaclass=ABCMeta):
    pass


class SynthesiserBase(MstSubObject, metaclass=ABCMeta):

    @abstractmethod
    def wave(self, hz: float, sec: float, **kwargs: t.Any) -> ndarray:
        pass

    @abstractmethod
    def play(self, wave_: ndarray, **kwargs: t.Any) -> None:
        pass

    @abstractmethod
    def save(self, path: str, wave_: ndarray, hz: float, **kwargs: t.Any) -> str:
        pass
