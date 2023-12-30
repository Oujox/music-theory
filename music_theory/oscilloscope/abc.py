from abc import abstractmethod
from ..mstobject import MstSubObject

class OscilloscopeBase(MstSubObject):

    @abstractmethod
    def display(self) -> None:
        pass