from .abc import TunerBase, ScaleBase


class JustIntonation(TunerBase):

    def __init__(self, root: float, scale: ScaleBase) -> None:
        self.root  = root
        self.scale = scale

    def hz(self, note_number: int) -> float:
        return 0.

class EqualTemperament(TunerBase):

    def __init__(self, root: float) -> None:
        self.root = root

    def hz(self, note_number: int) -> float:
        return self.root*2**((note_number-69)/12)