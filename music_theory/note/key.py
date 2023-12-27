import typing as t
from ._note import NoteBase


class Key:
    
    def __init__(self, name: str) -> None:

        self._name = NoteBase.from_notename(name)
        self._pos: int = self._name._dict_notenames.index(self.name)

    @property
    def name(self) -> str:
        return self._name.name
    
    @property
    def names(self):
        return self._name.names
    
    @property
    def pitchclass(self):
        return self._name.pitchclass
    
    def next(self, degree: int, mask: int) -> t.Self:
        name = self._name + degree
        return self.__class__(name._dict_notenames[mask+2])
    
    def __int__(self) -> int:
        return self._name.pitchclass
    
    def __str__(self) -> str:
        return "<Key: {}>".format(self._name.name)
    
    def __repr__(self) -> str:
        return "<Key: {}>".format(self._name.name)