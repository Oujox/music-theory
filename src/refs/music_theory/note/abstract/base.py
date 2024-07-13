
from abc import ABCMeta, abstractmethod
from .interface import *

class _Base(Displayable, Equatable, metaclass=ABCMeta): pass

class BaseNote(Ring, _Base):

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



class BaseScale(Ring, _Base):

    def __repr__(self) -> str:
        return super(object).__repr__()

    @property
    @abstractmethod
    def diatonic(self) -> list[BaseNote]:
        ...

    @property
    @abstractmethod
    def nondiatonic(self) -> list[BaseNote]:
        ...



class BaseTuner(_Base):

    def __eq__(self, value: object) -> bool:
        return super(object).__eq__(value)

    def __ne__(self, value: object) -> bool:
        return super(object).__ne__(value)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.root:.2f}hz>"

    def __repr__(self) -> str:
        return super(object).__repr__()

    @abstractmethod
    def hz(self, note_number: int) -> float:
        ...

