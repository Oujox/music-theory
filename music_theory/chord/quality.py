from __future__ import annotations
from ._const import NOTE2_QUALITIES, NOTE3_QUALITIES, NOTE4_QUALITIES


class Quality:
    
    def __init__(self, quality: str, append: str):
        self._name = quality
        self._degree = self.parse(quality, append)

    @classmethod
    def parse(cls, quality: str, append: str) -> list[int]|None:
        if quality in NOTE2_QUALITIES.keys():
            return [ a+b for a,b in zip([ 0, 4, 7, 11 ], NOTE2_QUALITIES[quality]) if b is not None ]

        if quality in NOTE3_QUALITIES.keys():
            return [ a+b for a,b in zip([ 0, 4, 7, 11 ], NOTE3_QUALITIES[quality]) if b is not None ]

        if quality in NOTE4_QUALITIES.keys():
            return [ a+b for a,b in zip([ 0, 4, 7, 11 ], NOTE4_QUALITIES[quality]) if b is not None ]