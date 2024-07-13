"""NoteMidi and NoteOctave"""
from __future__ import annotations

import re
import typing as t

from .abstract import BaseNote, BaseScale, BaseTuner
from .abstract import MixinScale
from .tuner import Equal12Tuner
from ._statics import NOTENAME_TO_PITCH, PITCH_TO_NOTENAME, ALL_NOTENAME

OCTAVE_NUMBER = 12
MIDI_NUMBER = 128

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


class NoteOctave(MixinScale, BaseNote):
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
    def __init__(
            self,
            pitchclass: int,
            *,
            scale: t.Optional[BaseScale] = None,
            **kwargs
            ) -> None:

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

    def __eq__(self, other: int|NoteOctave) -> bool:
        return self._pitchclass == int(other)

    def __ne__(self, other: int|NoteOctave) -> bool:
        return self._pitchclass != int(other)

    def __add__(self, other: int) -> NoteOctave:
        if other:
            return NoteOctave((self._pitchclass + other)%OCTAVE_NUMBER, scale=self.scale)
        return NoteOctave(self._pitchclass, scale=self.scale, _name=self.name)

    def __sub__(self, other: int) -> NoteOctave:
        if other:
            return NoteOctave((self._pitchclass - other)%OCTAVE_NUMBER, scale=self.scale)
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
        return isinstance(pitchclass, int) and 0 <= pitchclass < OCTAVE_NUMBER


class NoteMidi(NoteOctave):
    """
    Data that provides a basic representation of note on the Midi standard

    Parameters
    ----------
    note_number : int
        note_number in midi standard ( 0 ~ 127 )
    scale : Scale
        select a subclass of ``scale.ScaleBase`` containing note
    tuner : TunerBase
        select a subclass of ``tuner.TunerBase``

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
            scale: t.Optional[BaseScale] = None,
            tuner: BaseTuner = Equal12Tuner(440),
            **kwargs
            ) -> None:

        if not self.is_notenumber(note_number):
            raise ValueError("")

        self._number: int = note_number
        self.tuner  : BaseTuner = tuner

        super().__init__(
            note_number%OCTAVE_NUMBER,
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
    def name(self) -> str|None:
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
        names = [ n + str(self.pitch) for n in super().names ]

        if self.pitchclass == 0 and self.pitch == -1:
            return names[:-1]

        if self.pitchclass == 7 and self.pitch == 9:
            return names[1:]

        return names

    @property
    def pitch(self) -> int:
        """Get the pitch of the note.

        Returns:
            int: The pitch of the note.
        """
        return self._number//OCTAVE_NUMBER - 1

    @property
    def hz(self) -> float:
        """Get the frequency of the note in Hertz.

        Returns:
            float: The frequency of the note in Hertz
        """
        return self.tuner.hz(self._number)

    def __eq__(self, other: int | NoteMidi) -> bool:
        return self._number == int(other)

    def __ne__(self, other: int | NoteMidi) -> bool:
        return self._number != int(other)

    def __lt__(self, other: int | NoteMidi) -> bool:
        return self._number < int(other)

    def __gt__(self, other: int | NoteMidi) -> bool:
        return self._number > int(other)

    def __le__(self, other: int | NoteMidi) -> bool:
        return self._number <= int(other)

    def __ge__(self, other: int | NoteMidi) -> bool:
        return self._number >= int(other)

    def __add__(self, other: int) -> NoteMidi:
        return NoteMidi(
            self._number + other,
            scale=self.scale,
            tuner=self.tuner
            )

    def __sub__(self, other: int) -> NoteMidi:
        return NoteMidi(
            self._number - other,
            scale=self.scale,
            tuner=self.tuner
            )

    def __matmul__(self, other: int) -> NoteMidi:
        return NoteMidi(
            self._number + other*OCTAVE_NUMBER,
            scale=self.scale,
            tuner=self.tuner
            )

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

    def as_octave(self) -> NoteOctave:
        """Returns the equivalent NoteOctave for the NoteMidi object.

        Returns:
            NoteOctave: The equivalent NoteOctave for the NoteMidi object.
        """
        return NoteOctave(self.pitchclass, scale=self.scale)

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
            return cls(pitchclass + (int(pitch)+1)*OCTAVE_NUMBER, _name=notename, **kwargs)

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
        match     = re.match(notename_ptn, name)
        notename  = name[:match.end()]
        pitch     = name[match.end():]

        if super().is_notename(notename):
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
        return isinstance(note_number, int) and 0 <= note_number < MIDI_NUMBER
