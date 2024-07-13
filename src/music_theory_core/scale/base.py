
from abc import abstractmethod
from ..core import ObjectMT, Ring
from ..note.base import BaseNote


class BaseScale(Ring, ObjectMT):

    def __eq__(self, value: object) -> bool:
        return super(object).__eq__(value)

    def __ne__(self, value: object) -> bool:
        return super(object).__ne__(value)

    def __repr__(self) -> str:
        return super(object).__repr__()

    @property
    @abstractmethod
    def diatonic(self) -> list[BaseNote]:
        ...

    @property
    @abstractmethod
    def non_diatonic(self) -> list[BaseNote]:
        ...
