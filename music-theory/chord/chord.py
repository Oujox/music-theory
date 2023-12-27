from __future__ import annotations

import re
import typing as t

from note import Note, NoteBase
from .quality import Quality


notename_ptn = re.compile(r"[A-Z][#b]?")
add_ptn = re.compile(r"add([-+b#]?9|[+#]?11|[-b]?13)")
tension_ptn = re.compile(r"([-+b#]?9|[+#]?11|[-b]?13)+")
onchord_ptn = re.compile(r"\/[A-Z][#b]?")


class Chord:

    def __init__(self, name: str):
        self._name = name

        # parse chord
        r, q, a, o = self.parse(name)
        self._root = r
        self._quality = Quality(q, a)
        self._on = o


    @classmethod
    def parse(cls, name: str) -> tuple[str, str, str, str]:
        name = name.replace(" ", "")

        # root note
        if not cls.is_rootname(name):
            raise ValueError()
        r = re.match(notename_ptn, name)
        name = name[r.end():]
        r = r.group()
        
        # onchord note
        o = re.search(onchord_ptn, name)
        if o is not None:
            name = name[:o.start()]
            o = o.group()[1:]
        
        # append quality
        a = re.search(add_ptn, name)
        if a is not None:
            name = name[:a.start()] + name[a.end():]
            a = a.group()
        else:
            a = re.search(tension_ptn, name)
            if a is not None:
                name = name[:a.start()] + name[a.end():]
                a = a.group()

        return r, name, a, o
    
    @classmethod
    def is_rootname(cls, name: str) -> t.TypeGuard[str]:
        return NoteBase.is_notename(re.match(notename_ptn, name).group())
        