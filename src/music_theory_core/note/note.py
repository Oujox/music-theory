
import re
import typing as t

from ..core import ObjectMT

from .base import BaseNote
from ..scale.base import BaseScale



class NoteOctave(BaseNote, ObjectMT, st=12):
    """
    Data that provides a basic representation of note on the octave

    Parameters
    ----------
    picthclass : int
        sequential number with C as 0 ( 0 ~ 12 )
    scale : Scale
        select a ``scale.Scale`` containing note

    See Also
    --------
    NoteOctave.from_notename : Constructor from notename.

    Examples
    --------
    Constructing NoteOctave from a pitchclass.

      >>> n_num = 0  # pitchclass number
      >>> c = NoteOctave(pitchclass=n_num)
      >>> c
      ['Dbb', 'C', 'B#']

    Constructing NoteOctave from a notename.

      >>> note_name = "C"
      >>> c = NoteOctave.from_notename(name=note_name)
      >>> c
      'C'

    """
    def __init__(self, pitchclass: int, *, scale: t.Optional[BaseScale] = None, **kwargs) -> None:

        if not self.is_pitchclass(pitchclass):
            raise ValueError("")

        self._pitchclass: int = pitchclass
        self._name: t.Optional[str] = kwargs.pop("_name", None)

        super().__init__(pitchclass, scale=scale, **kwargs)

    @property
    def pitchclass(self) -> int:
        """Returns the pitch class of the note.

        Returns:
            int: The pitch class of the note.
        """
        return self._pitchclass

    @property
    def name(self) -> t.Optional[str]:
        """Returns the name of the note.

        Returns:
            str|None: The name of the note, or None if the note does not have a name.
        """
        return self._name

    @property
    def names(self) -> list[str]:
        """Get the note names.

        Returns:
            list[str]: The note names.
        """
        return [ n for n in self.names_sequence if n is not None]

    @property
    def names_sequence(self) -> tuple[t.Optional[str]]:
        """Returns the sequence of note names for the pitch class of the note.

        Returns:
            list[str]: The sequence of note names for the pitch class of the note.
        """
        return PITCH_TO_NOTENAME[self._pitchclass]

    def __setattr__(self, __name: str, __value: t.Any) -> None:
        if __name == "scale" and isinstance(__value, BaseScale):
            self.__update_notename_by_scale(__value)
        return super().__setattr__(__name, __value)

    def __eq__(self, other: int|"NoteOctave") -> bool:
        return self._pitchclass == int(other)

    def __ne__(self, other: int|"NoteOctave") -> bool:
        return self._pitchclass != int(other)

    def __add__(self, other: int) -> "NoteOctave":
        if other:
            return NoteOctave((self._pitchclass + other)%self.SEMITONES, scale=self.scale)
        return NoteOctave(self._pitchclass, scale=self.scale, _name=self.name)

    def __sub__(self, other: int) -> "NoteOctave":
        if other:
            return NoteOctave((self._pitchclass - other)%self.SEMITONES, scale=self.scale)
        return NoteOctave(self._pitchclass, scale=self.scale, _name=self.name)

    def __int__(self) -> int:
        return self._pitchclass

    def __str__(self) -> str:
        return self.name if self.name is not None else str(self.names)

    def __repr__(self) -> str:
        return self.name if self.name is not None else str(self.names)

    def __update_notename_by_scale(self, scale: BaseScale) -> None:
        note = scale.diatonic[0]+self.pitchclass
        self._name = scale.nondiatonic[note.pitchclass].name

    @classmethod
    def from_notename(cls, name: str, **kwargs) -> t.Self:
        """
        Create a NoteOctave object from a note name.

        Parameters
        ----------
        name : str
            The note name, e.g. 'C', 'Db', 'F#', etc.
        kwargs
            Additional keyword arguments to pass to the NoteOctave constructor.

        Returns
        -------
        NoteOctave
            The NoteOctave object.

        Raises
        ------
        ValueError
            If the note name is not valid.
        """
        if not cls.is_notename(name):
            raise ValueError(f"there is no notename called {name}.")
        return cls(NOTENAME_TO_PITCH[name], _name=name, **kwargs)

    @classmethod
    def is_notename(cls, name: str) -> t.TypeGuard[str]:
        """
        This function determines if the input is a valid note name.

        Parameters
        ----------
        name : str
            The note name to be checked.

        Returns
        -------
        bool
            ``True`` if the input is a valid note name, ``False`` otherwise.
        """
        return isinstance(name, str) and name in cls

    @classmethod
    def is_pitchclass(cls, pitchclass: int) -> t.TypeGuard[int]:
        """
        This function determines if the input is a valid pitch class.

        Parameters
        ----------
        pitchclass : int
            The pitch class to be checked.

        Returns
        -------
        bool
            ``True`` if the input is a valid pitch class, ``False`` otherwise.
        """
        return isinstance(pitchclass, int) and 0 <= pitchclass < cls.SEMITONES

