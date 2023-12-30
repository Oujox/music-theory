from abc import abstractmethod
from ..mst_object import MstSubObject

class OscilloscopeBase(MstSubObject):

    @abstractmethod
    def display(self) -> None:
        pass