from abc import ABCMeta, abstractmethod

from ..note import NoteMod


class TunerObject(NoteMod, metaclass=ABCMeta):

    def __init__(self, root: int):
        self.root: int = root
    
    @abstractmethod
    def hz(self, note_number: int) -> float:
        pass
