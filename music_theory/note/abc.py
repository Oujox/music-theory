"""Base classes"""
from abc import abstractmethod, abstractproperty
from ..mst_object import MstMainObject, MstSubObject


class NoteBase(MstMainObject):
    """Abstract base class for notes."""
    @property
    @abstractproperty
    def pitchclass(self) -> int:
        """must override in subclasses"""


class ScaleBase(MstSubObject):
    """Abstract base class for scales."""
    @property
    @abstractproperty
    def diatonic(self) -> list[NoteBase]:
        """must override in subclasses"""


class TunerBase(MstSubObject):
    """Abstract base class for tuners."""
    @abstractmethod
    def hz(self, note_number: int) -> float:
        pass