""" define base classes
"""

from abc import ABCMeta

from ..utils.interface import Displayable, Equatable
from .domain import DomainMT



class BaseMT(Displayable, Equatable, metaclass=ABCMeta):
    """
    """


class ObjectMT(DomainMT, BaseMT):
    """
    """
