from numpy import ndarray
from ..note import NoteHandlerProxy

class SynthesiserHandler(NoteHandlerProxy):

    def __init__(self, note_number: int, **kwargs) -> None:
        # mods
        from .synthesiser import SynthesiserObject
        self.synthe: SynthesiserObject = kwargs.pop("synthe", None)
        
        from ..tuner import TunerHandler
        if not TunerHandler in self.__class__.mro():
            raise NotImplementedError("TunerHandler が継承されていない.")
        
        super().__init__(note_number, **kwargs)
    
    def wave(self, sec: float = 1, **kwargs) -> ndarray:
        wave = self.synthe.wave(self.hz, sec)
        if kwargs.pop("sound", False):
            self.synthe.sound(wave, **kwargs)
        if (save := kwargs.pop("save", None)) is not None:
            self.synthe.save(save, wave, self.hz, **kwargs)
        return wave
    
    def _wave(self, **kwargs) -> ndarray:
        wave = self.synthe.wave(self.hz, 1/self.hz)
        if kwargs.pop("sound", False):
            self.synthe.sound(wave, **kwargs)
        if (path := kwargs.pop("path", None)) is not None:
            self.synthe.save(path, wave, self.hz, **kwargs)
        return wave