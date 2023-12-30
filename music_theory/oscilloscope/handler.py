from .abc import OscilloscopeBase
from ..tone import ToneHandler


class OscilloscopeHandler(ToneHandler):

    def __init__(self, note_number: int, **kwargs) -> None:
        # mstsubobj
        self.scope: OscilloscopeBase = kwargs.pop("scope", None)

        super().__init__(note_number, **kwargs)