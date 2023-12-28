from abc import ABCMeta, abstractmethod

from ..mst_object import MstModObject


class TunerObject(MstModObject, metaclass=ABCMeta):

    def __init__(self, root: int):
        self.root: int = root

    @abstractmethod
    def hz(self, note_number: int) -> float:
        pass
