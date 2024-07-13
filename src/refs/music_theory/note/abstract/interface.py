
import typing as t
from abc import abstractmethod
from collections.abc import Collection

class Ring(Collection):
    @abstractmethod
    def __int__(self) -> int:
        ...

    @abstractmethod
    def __add__(self, other: t.Self) -> t.Self:
        ...

    @abstractmethod
    def __sub__(self, other: t.Self) -> t.Self:
        ...

class Displayable:
    @abstractmethod
    def __str__(self) -> str:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...

class Equatable:
    @abstractmethod
    def __lt__(self, other: t.Self) -> bool:
        ...

    @abstractmethod
    def __le__(self, other: t.Self) -> bool:
        ...

class Orderable:
    @abstractmethod
    def __lt__(self, other: t.Self) -> bool:
        ...

    @abstractmethod
    def __le__(self, other: t.Self) -> bool:
        ...

    @abstractmethod
    def __gt__(self, other: t.Self) -> bool:
        ...

    @abstractmethod
    def __ge__(self, other: t.Self) -> bool:
        ...

