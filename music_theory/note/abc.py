"""Base classes"""
from abc import abstractproperty
from ..mst_object import MstObject


class NoteBase(MstObject):
    """Abstract base class for notes."""
    @property
    @abstractproperty
    def pitchclass(self) -> int:
        """must override in subclasses"""


class ScaleBase(MstObject):
    """Abstract base class for scales."""
    @property
    @abstractproperty
    def diatonic(self) -> list[NoteBase]:
        """must override in subclasses"""
