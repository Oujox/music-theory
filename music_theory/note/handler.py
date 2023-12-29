import typing as t
from .note import NoteMidi


class NoteHandlerProxy(NoteMidi):
    """
    """

    def __add__(self, other: int) -> t.Self:
        return self.__class__(self._number + other, **self.mst_subs)

    def __sub__(self, other: int) -> t.Self:
        return self.__class__(self._number - other, **self.mst_subs)

    def __matmul__(self, other: int) -> t.Self:
        return self.__class__(self._number + other*12, **self.mst_subs)
