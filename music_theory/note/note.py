from __future__ import annotations

import typing as t
from .abc import Scale
from ._statics import NOTENAME_TO_PITCH, PITCH_TO_NOTENAME, ALL_NOTENAME

from ..mst_object import MstObject


class NoteBase(MstObject):

    def __init__(self, pitchclass: int, **kwargs) -> None:

        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"pitchclass において {pitchclass} は範囲外です.")

        self._pitchclass: int = pitchclass
        self._name: str|None = kwargs.pop("_name", None)
        self.scale: Scale|None = kwargs.pop("scale", None)

    @property
    def name(self) -> str|None:
        return self._name

    @property
    def names(self) -> list[str]:
        return [ n for n in PITCH_TO_NOTENAME[self.pitchclass] if n is not None]

    @property
    def pitchclass(self) -> int:
        return self._pitchclass

    @property
    def names_sequence(self):
        return PITCH_TO_NOTENAME[self._pitchclass]

    def __eq__(self, other: int|NoteBase) -> bool:
        return self._pitchclass == int(other)

    def __ne__(self, other: int|NoteBase) -> bool:
        return self._pitchclass != int(other)

    def __add__(self, other: int) -> t.Self:
        return self.__class__((self._pitchclass + other)%12)

    def __sub__(self, other: int) -> t.Self:
        return self.__class__((self._pitchclass - other)%12)

    def __int__(self) -> int:
        return self._pitchclass

    def __str__(self) -> str:
        return str(self._name)

    def __repr__(self) -> str:
        return str(self._name)

    def __setattr__(self, __name: str, __value: t.Any) -> None:
        if __name == "scale" and isinstance(__value, Scale):
            self._update_notename_by_scale(__value)
        super().__setattr__(__name, __value)

    def _update_notename_by_scale(self, scale):
        names = set([ n for n in self.names_sequence if n is not None])
        diatonic = set([ k.name for k in scale.diatonic ])
        self._name = name[0] if len((name := list(names & diatonic))) == 1 else None

    @classmethod
    def from_notename(cls, name: str, **kwargs) -> t.Self:
        if not cls.is_notename(name):
            raise ValueError(f"<Note: {name}> は存在しません.")
        return cls(NOTENAME_TO_PITCH[name], _name=name, **kwargs)

    @classmethod
    def is_notename(self, name: str) -> t.TypeGuard[str]:
        return isinstance(name, str) and name in ALL_NOTENAME

    @classmethod
    def is_pitchclass(cls, pitchclass: int) -> t.TypeGuard[int]:
        return isinstance(pitchclass, int) and 0 <= pitchclass < 12


class Note(NoteBase):

    """
    Data to provide many ways of expressing things about note

    Parameters
    ----------
    note_number : int
        note_number in midi standard
    tuner : TunerObject
        Tuner object provided by ``note.tuner``
    synthe : SynthesiserObject
        Synthesiser object provided by ``note.synthe``

    See Also
    --------
    Note.from_notename : Constructor from notename and pitch.

    Examples
    --------
    Constructing Note from a note_number.

      >>> n_num = 60  # is Dbb4, C4 or B#4
      >>> c4 = Note(note_number=n_num)
      >>> c4
      <Note: ['Dbb4', 'C4', 'B#4']; number: 60>

    Constructing Note from a notename.

      >>> n_name, n_pitch = "C", 4
      >>> c4 = Note.from_notename(name=n_name, picth=n_pitch)
      >>> c4

      >>> <Note: C4; number: 60>

    """

    def __init__(self, note_number: int, **kwargs) -> None:

        if not self.is_notenumber(note_number):
            raise ValueError("")
        self._number: int = note_number

        super().__init__( note_number%12, **kwargs )

    @property
    def number(self) -> int:
        return self._number

    @property
    def name(self) -> str|None:
        return super().name + str(self.pitch) if super().name is not None else None

    @property
    def names(self) -> list[str]:
        return [ n + str(self.pitch) for n in super().names ]

    @property
    def pitch(self) -> int:
        return self._number//12 - 1

    def __eq__(self, other: int|Note) -> bool:
        return self._number == int(other)

    def __ne__(self, other: int|Note) -> bool:
        return self._number != int(other)

    def __lt__(self, other: int|Note) -> bool:
        return self._number < int(other)

    def __gt__(self, other: int|Note) -> bool:
        return self._number > int(other)

    def __add__(self, other: int) -> Note:
        return Note(self._number + other)

    def __sub__(self, other: int) -> Note:
        return Note(self._number - other)

    def __matmul__(self, other: int) -> Note:
        return Note(self._number + other*12)

    def __int__(self) -> int:
        return self._number

    def __str__(self) -> str:
        return "<Note: {}; number: {}>".format(
            self.name if self._name is not None else str(self.names), 
            self._number
        )

    @classmethod
    def from_notename(cls, name: str, pitch: int = 4, **kwargs) -> t.Self:
        if not cls.is_notename(name, pitch):
            raise ValueError(f"<Note: {name}, pitch: {pitch}> は存在しません.")
        return cls(NOTENAME_TO_PITCH[name] + (pitch+1)*12, _name=name, **kwargs)

    @classmethod
    def is_notename(cls, name: str, pitch: int) -> bool:
        if super().is_notename(name):
            if 0 <= NOTENAME_TO_PITCH[name] < 8:
                return -1 <= pitch < 10
            else:
                return -1 <= pitch < 9
        return False

    @classmethod
    def is_notenumber(cls, note_number: int) -> t.TypeGuard[int]:
        return isinstance(note_number, int) and 0 <= note_number < 128
