from .abc import OscilloscopeBase
from ..synthesiser import SynthesiserHandler


class OscilloscopeHandler(SynthesiserHandler):

    def __init__(self, note_number: int, **kwargs) -> None:
        # mstsubobj
        self.scope: OscilloscopeBase = kwargs.pop("scope", None)

        super().__init__(note_number, **kwargs)