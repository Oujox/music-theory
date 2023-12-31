from .scope import Oscilloscope
from ..tone import ToneHandler


class OscilloscopeHandler(ToneHandler):

    def __init__(self, note_number: int, **kwargs) -> None:
        # mstsubobj
        self.scope: Oscilloscope = Oscilloscope()

        super().__init__(note_number, **kwargs)