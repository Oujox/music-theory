
from .chord import Chord
from ..note.scale import Scale


class Progress:

    def __init__(self, *chord: Chord, scale: Scale) -> None:
        self._progress = [ c(scale=scale) for c in chord ]

    @property
    def progress(self) -> list[Chord]:
        return self._progress
