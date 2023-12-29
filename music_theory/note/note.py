"""NoteMidi and NoteOctave"""
from __future__ import annotations

import re
import typing as t

from .abc import ScaleBase, NoteBase
from ._statics import NOTENAME_TO_PITCH, PITCH_TO_NOTENAME, ALL_NOTENAME

notename_ptn = re.compile(r"[A-G][b#]{0,2}")

def pitch_pitchclass_relation(pitch: int, pitchclass: int) -> bool:
    """
    This function determines if the pitch and pitch class of a note are consistent.

    Parameters
    ----------
    pitch : int
        The pitch.
    pitchclass : int
        The pitch class.

    Returns
    -------
    bool

    """
    if 0 <= pitchclass < 8:
        return -1 <= pitch < 10
    return -1 <= pitch < 9


class NoteOctave(NoteBase):
    """
    Data that provides a basic representation of note on the octave

    Parameters
    ----------
    picthclass : int
        sequential number with C as 0 ( 0 ~ 7 )
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
      'C4'

    """
    def __init__(
            self,
            pitchclass: int,
            *,
            scale: ScaleBase|None = None,
            **kwargs
            ) -> None:

        if not self.is_pitchclass(pitchclass):
            raise ValueError("")

        self._pitchclass: int = pitchclass
        self._scale: ScaleBase|None = scale
        self._name : str|None = kwargs.pop("_name", None)

        if isinstance(self._scale, ScaleBase):
            self.__update_notename_by_scale(self._scale)

    @property
    def name(self) -> str|None:
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
        return [ n for n in PITCH_TO_NOTENAME[self.pitchclass] if n is not None]

    @property
    def pitchclass(self) -> int:
        """Returns the pitch class of the note.

        Returns:
            int: The pitch class of the note.
        """
        return self._pitchclass

    @property
    def names_sequence(self) -> tuple[str|None]:
        """Returns the sequence of note names for the pitch class of the note.

        Returns:
            list[str]: The sequence of note names for the pitch class of the note.
        """
        return PITCH_TO_NOTENAME[self._pitchclass]

    @property
    def scale(self) -> ScaleBase|None:
        """Set the scale of the note.

        Args:
            scale (Scale): The scale to set.

        Raises:
            ValueError: If the scale is not an instance of Scale.
        """
        return self._scale

    @scale.setter
    def scale(self, scale: ScaleBase) -> None:
        self._scale = scale
        self.__update_notename_by_scale(scale)

    def __eq__(self, other: int|NoteOctave) -> bool:
        return self._pitchclass == int(other)

    def __ne__(self, other: int|NoteOctave) -> bool:
        return self._pitchclass != int(other)

    def __add__(self, other: int) -> NoteOctave:
        return NoteOctave((self._pitchclass + other)%12, scale=self._scale)

    def __sub__(self, other: int) -> NoteOctave:
        return NoteOctave((self._pitchclass - other)%12, scale=self._scale)

    def __int__(self) -> int:
        return self._pitchclass

    def __str__(self) -> str:
        return self.name if self.name is not None else str(self.names)

    def __repr__(self) -> str:
        return self.name if self.name is not None else str(self.names)

    def __update_notename_by_scale(self, scale: ScaleBase) -> None:
        names    = frozenset([ n for n in self.names_sequence if n is not None])
        diatonic = frozenset([ k.name for k in scale.diatonic ])
        self._name = name[0] if len((name := list(names & diatonic))) == 1 else None

    @classmethod
    def from_notename(cls, name: str, **kwargs) -> NoteOctave:
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
        return isinstance(name, str) and name in ALL_NOTENAME

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
        return isinstance(pitchclass, int) and 0 <= pitchclass < 12


class NoteMidi(NoteOctave):
    """
    Data that provides a basic representation of note on the Midi standard

    Parameters
    ----------
    note_number : int
        note_number in midi standard ( 0 ~ 127 )
    scale : Scale
        select a ``scale.Scale`` containing note

    See Also
    --------
    NoteMidi.from_notename : Constructor from notename and pitch.

    Examples
    --------
    Constructing NoteMidi from a note_number.

      >>> n_num = 60  # midi number
      >>> c4 = NoteMidi(note_number=n_num)
      >>> c4

      >>> <Note: ['Dbb4', 'C4', 'B#3']; number: 60>

    Constructing NoteMidi from a notename.

      >>> note_name = "C4"
      >>> c4 = NoteMidi.from_notename(name=note_name)
      >>> c4

      >>> <Note: C4; number: 60>

    """
    def __init__(
            self,
            note_number: int,
            *,
            scale: ScaleBase = None,
            **kwargs
            ) -> None:

        if not self.is_notenumber(note_number):
            raise ValueError("")
        self._number: int = note_number

        super().__init__(
            note_number%12,
            scale=scale,
            **kwargs
            )

    @property
    def number(self) -> int:
        """Returns the MIDI note number of the note.

        Returns:
            int: The MIDI note number of the note.
        """
        return self._number

    @property
    def name(self) -> str | None:
        """Get the note name.

        Returns:
            str: The note name. If the note does not have a name, returns None.
        """
        return super().name + str(self.pitch) if super().name is not None else None

    @property
    def names(self) -> list[str]:
        """Get the note names.

        Returns:
            list[str]: The note names.
        """
        if self.pitchclass == 0:
            return [ n + str(self.pitch - int(i == 2)) for i, n in enumerate(super().names) ]
        if self.pitchclass == 11:
            return [ n + str(self.pitch + int(i == 0)) for i, n in enumerate(super().names) ]
        return [ n + str(self.pitch) for n in super().names ]

    @property
    def pitch(self) -> int:
        """Get the pitch of the note.

        Returns:
            int: The pitch of the note.
        """
        return self._number//12 - 1

    def __eq__(self, other: int | NoteMidi) -> bool:
        return self._number == int(other)

    def __ne__(self, other: int | NoteMidi) -> bool:
        return self._number != int(other)

    def __lt__(self, other: int | NoteMidi) -> bool:
        return self._number < int(other)

    def __gt__(self, other: int | NoteMidi) -> bool:
        return self._number > int(other)

    def __add__(self, other: int) -> NoteMidi:
        return NoteMidi(self._number + other)

    def __sub__(self, other: int) -> NoteMidi:
        return NoteMidi(self._number - other)

    def __matmul__(self, other: int) -> NoteMidi:
        return NoteMidi(self._number + other*12)

    def __int__(self) -> int:
        return self._number

    def __str__(self) -> str:
        return "<NoteMidi: {}; number: {}>".format(
            self.name if self.name is not None else str(self.names),
            self._number
        )

    def __repr__(self) -> str:
        return "<NoteMidi: {}; number: {}>".format(
            self.name if self.name is not None else str(self.names),
            self._number
        )

    @classmethod
    def from_notename(cls, name: str, **kwargs) -> t.Self:
        """
        Create a NoteMidi object from a note name.

        Parameters
        ----------
        name : str
            The note name, e.g. 'C4', 'Db4', 'F#5', etc.
        kwargs
            Additional keyword arguments to pass to the NoteMidi constructor.

        Returns
        -------
        NoteMidi
            The NoteMidi object.

        Raises
        ------
        ValueError
            If the note name is not valid.
        """
        match      = re.match(notename_ptn, name)
        notename   = name[:match.end()]
        pitch      = name[match.end():]
        pitchclass = NOTENAME_TO_PITCH[notename]

        if super().is_notename(notename):
            if not pitch_pitchclass_relation(int(pitch), pitchclass):
                raise ValueError(f"{notename} cannot exist if pitch is {pitch}.")
            return cls(pitchclass + (int(pitch)+1)*12, _name=notename, **kwargs)

        else:
            raise ValueError(f"there is no notename called {name}.")

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
        if super().is_notename(name):
            match     = re.match(notename_ptn, name)
            notename  = name[:match.end()]
            pitch     = name[match.end():]

            return pitch_pitchclass_relation(int(pitch), NOTENAME_TO_PITCH[notename])
        return False

    @classmethod
    def is_notenumber(cls, note_number: int) -> t.TypeGuard[int]:
        """
        This function determines if the input is a valid MIDI note number.

        Parameters
        ----------
        note_number : int
            The MIDI note number to be checked.

        Returns
        -------
        bool
            ``True`` if the input is a valid MIDI note number, ``False`` otherwise.
        """
        return isinstance(note_number, int) and 0 <= note_number < 128
