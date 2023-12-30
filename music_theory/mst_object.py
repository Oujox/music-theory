"""
MstObject
---------

Abstract base class for MST objects
  1. Provide a variety of output formats
  2. Clearly distinguish it from other objects
"""


from abc import ABCMeta

class MstObject(metaclass=ABCMeta):
    """
    Abstract base class for MST objects
    """


class MstSubObject(MstObject):
    """
    """


class MstMainObject(MstObject):
    """
    """
    @property
    def mst_subs(self) -> dict[str, MstSubObject]:
        return dict(
            *[ [k, v] for k, v in self.__dict__.items() if isinstance(v, MstSubObject)]
        )