
from __future__ import annotations

import re
import typing as t

from ..note import NoteOctave, OCTAVE_NUMBER
from ..note.abstract import BaseScale
from ..note.abstract import MixinScale
from .quality import Quality

ptn_root = re.compile(r"[A-G](b|#)?")
ptn_on   = re.compile(r"/[A-G](b|#)?")


class Chord(MixinScale):
    """
     Data that provides a representation of the code in music theory

    Parameters
    ----------
    chord : str
        chord string
    scale : Scale
        select a ``scale.Scale`` containing chord components

    Examples
    --------
    Constructing NoteOctave from normal chord.

      >>> chord = "Cm7b5"
      >>> c = Chord(chord=chord)
      >>> c
      <Chord: Cm7b5>

    Constructing NoteOctave from inversion chord.

      >>> chord = "Cm7b5/Eb"
      >>> c = Chord(chord=chord)
      >>> c, c.degree
      <Chord: Cm7b5/Eb> [0, 3, 7, 9]

    Constructing NoteOctave from on chord.

      >>> chord = "Cm7b5/D"
      >>> c = Chord(chord=chord)
      >>> c, c.degree
      <Chord: Cm7b5/D> [0, 10, 13, 16, 20]

    """

    def __init__(
            self,
            chord: str,
            *,
            scale: t.Optional[BaseScale] = None,
            **kwargs: t.Any
            ):

        root, on, quality, number = self.parse(chord, scale)
        self._root = root
        self._on = on
        self._quality = Quality(quality, number)

        super().__init__(chord, scale=scale, **kwargs)

    @property
    def root(self) -> NoteOctave:
        return self._root

    @property
    def on(self) -> t.Optional[NoteOctave]:
        return self._on

    @property
    def notes(self) -> int:
        return self._quality.notes

    @property
    def degree(self) -> list[int]:
        return self._quality.degree

    @property
    def components(self) -> list[NoteOctave]:
        if self._quality.isonchord() or self._quality.isinvchord():
            return [ self.on + d for d in self.degree ]
        return [ self.root + d for d in self.degree ]

    @root.setter
    def root(self, root: str):
        self._root = NoteOctave.from_notename(root, scale=self.scale)
        self.__update_quality()

    @on.setter
    def on(self, on: str):
        self._on = NoteOctave.from_notename(on, scale=self.scale)
        self.__update_quality()

    def __eq__(self, other: t.Self) -> bool:
        r = self.root == other.root
        q = self._quality == other._quality
        return r & q

    def __ne__(self, other: t.Self) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        if self._quality.isonchord() or self._quality.isinvchord():
            return f"{self.root.name}{self._quality}/{self.on.name}"
        return f"{self.root.name}{self._quality}"

    def __repr__(self) -> str:
        return f"<Chord: {self.__str__()}>"

    def inversion(self, rotate: int) -> None:
        self._quality.inversion(rotate)

    def __update_quality(self):
        number = 0
        if self._on is not None:
            number = (int(self._on) - int(self._root))%OCTAVE_NUMBER
        self._quality = Quality(self._quality.quality, number)

    @classmethod
    def parse(self, chord: str, scale: BaseScale):
        mrt = re.match(ptn_root, chord)
        mon = re.search(ptn_on, chord)
        rt = NoteOctave.from_notename(mrt.group(), scale=scale)

        if (c := chord.count("(")) == chord.count(")") and c > 0:
            chord = chord.replace("(", "")
            chord = chord.replace(")", "")
        if mon is None:
            return rt, None, chord[mrt.end():], 0

        on = NoteOctave.from_notename(mon.group()[1:], scale=scale)
        number = (int(on) - int(rt))%OCTAVE_NUMBER
        quality = chord[mrt.end():mon.start()]
        return rt, on, quality, number

