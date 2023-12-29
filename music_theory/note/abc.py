"""Base classes"""
from abc import abstractproperty
from ..mst_object import MstObject


class NoteBase(MstObject):
    """Abstract base class for notes."""
    @property
    @abstractproperty
    def pitchclass(self) -> int:
        """
        The pitch class of the note.

        Returns
        -------
        int
            The pitch class of the note.
        """

class ScaleBase(MstObject):
    """Abstract base class for scales."""
    @property
    @abstractproperty
    def diatonic(self) -> list[NoteBase]:
        """
        The diatonic notes of the scale.

        Returns
        -------
        list
            The diatonic notes of the scale.
        """
