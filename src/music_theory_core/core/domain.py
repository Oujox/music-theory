""" define domain
"""
import typing as t

class DomainMT: # pylint: disable=too-few-public-methods
    """
    音楽理論の基礎概念を提供する
    ---

    ライブラリ内ではすべてのMTオブジェクトがこのドメインを継承する.
    以下を基礎概念とする.

    1. オクターブの等価性
    2. オクターブは

    Parameters
    ---
    semitones : int
        Number of divisions per octave. Normally, 12 would be used.

    Notes
    ---
    Instantiation not possible.
    This superclass is used only to subdivide class definitions.
    """

    # Octave Equivalence
    OVERTONE: t.Final[int]
    DIATONIC: t.Final[int]
    SEMITONES: t.Final[int]

    def __init_subclass__(cls, **kwargs) -> None:
        cls.OVERTONE = kwargs.pop("overtone", None)
        cls.DIATONIC = kwargs.pop("diatonic", None)
        cls.SEMITONES = kwargs.pop("semitones", None)
        return super().__init_subclass__(**kwargs)
