
from abc import abstractmethod
from ..interface import Ring


class BaseNote(Ring):

    def __repr__(self) -> str:
        return super(object).__repr__()

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def pitchclass(self) -> int:
        ...
