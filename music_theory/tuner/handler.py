from .tuner import TunerObject
from ..note import NoteHandlerProxy


class TunerHandler(NoteHandlerProxy):

    def __init__(self, note_number: int, **kwargs) -> None:
        # mods
        self.tuner: TunerObject = kwargs.pop("tuner", None)

        super().__init__(note_number, **kwargs)

    @property
    def hz(self) -> float:
        return self.tuner.hz(self._number)