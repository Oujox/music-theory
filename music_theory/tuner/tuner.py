from ..note.scale import ScaleBase
from .abc import TunerObject

class JustIntonation(TunerObject):

    def hz(self, note_number: int, scale: ScaleBase) -> float:
        return 

class EqualTemperament(TunerObject):
    
    def hz(self, note_number: int) -> float:
        return self.root*2**((note_number-69)/12)
        