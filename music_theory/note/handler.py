import typing as t
from .mod import NoteMod
from .note import Note

class NoteHandlerProxy(Note):
    """
    """

    @property
    def mods(self) -> dict[str, NoteMod]:
        return dict(
            [ [k, v] for k, v in self.__dict__.items() if isinstance(v, NoteMod)]
        )

    def __add__(self, other: int) -> t.Self:
        return self.__class__(self._number + other, **self.mods)

    def __sub__(self, other: int) -> t.Self:
        return self.__class__(self._number - other, **self.mods)

    def __matmul__(self, other: int) -> t.Self:
        return self.__class__(self._number + other*12, **self.mods)
