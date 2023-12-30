from numpy import ndarray

from .synthesiser import ToneBase
from ..note import NoteHandlerProxy


class ToneHandler(NoteHandlerProxy):

    def __init__(self, note_number: int, **kwargs) -> None:
        # mstsubobj
        self.synthe: ToneBase = kwargs.pop("synthe", None)

        super().__init__(note_number, **kwargs)

    def wave(self, sec: float = 1, **kwargs) -> ndarray:
        wave = self.synthe.wave(self.hz, sec)
        if kwargs.pop("play", False):
            self.synthe.play(wave, **kwargs)
        if (save := kwargs.pop("save", None)) is not None:
            self.synthe.save(save, wave, self.hz, **kwargs)
        return wave

    def wave_forsound(self, **kwargs) -> ndarray:
        wave = self.synthe.wave(self.hz, 1/self.hz)
        if kwargs.pop("play", False):
            self.synthe.play(wave, **kwargs)
        if (path := kwargs.pop("path", None)) is not None:
            self.synthe.save(path, wave, self.hz, **kwargs)
        return wave