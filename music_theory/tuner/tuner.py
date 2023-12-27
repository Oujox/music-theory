from ..note.scale import Scale
from .abc import TunerObject

class JustIntonation(TunerObject):

    def hz(self, note_number: int, scale: Scale) -> float:
        return 

class EqualTemperament(TunerObject):
    
    def hz(self, note_number: int) -> float:
        return self.root*2**((note_number-69)/12)
        