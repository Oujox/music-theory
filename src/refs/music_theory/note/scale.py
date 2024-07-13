
import typing as t
import functools

from .abstract import BaseScale
from .key import Key
from .note import NoteOctave
from ._statics import BASE_INTERVAL, CODETONE_SYMBOLS


def count_flat_sharp(key: Key) -> int:
    if key.fifth == 6:
        return key.fifth - 12 if key.fifth > int(key.accsidental == 1) + 5 else key.fifth
    else:
        return key.fifth - 12 if key.fifth > 5 else key.fifth

def generate_mask_by_key(key: Key) -> list[int]:
    fs_count = count_flat_sharp(key)
    mask = [0]*7
    if fs_count > 0:
        for i in range(0, fs_count):
            mask[-((i*4)%7+1)] = 1
    elif fs_count < 0:
        for i in range(1, -fs_count+1):
            mask[(i*4)%7-1] = -1
    return mask

def _interpreted_diatonic_elements(accidental: tuple[t.Optional[int]], mask: list[int]) -> tuple[list[int]]:
    _accidental = [ v for v in accidental if v is not None ]
    _mask = [ mask[i] for i, v in enumerate(accidental) if v is not None ]
    return _accidental, _mask


class Scale(BaseScale):

    interval: t.ClassVar[tuple[int]]

    def __init__(self, key: str|Key):
        self.key = key if isinstance(key, Key) else Key(key)
        self.policy = 1 if self.key.accsidental == 0 else self.key.accsidental

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def degree(self) -> list[int]:
        return [ sum(self.interval[:i]) for i in range(len(self.interval)) ]

    @property
    def diatonic(self) -> list[NoteOctave]:
        return self._diatonic(self.key)

    @property
    def nondiatonic(self) -> list[NoteOctave]:
        return self._nondiatonic(self.key)

    @property
    def codetone(self) -> dict[str, str]:
        return dict([ (CODETONE_SYMBOLS[de], di) for de, di in zip(self.degree, self.diatonic)])

    @functools.lru_cache(maxsize=None)
    def _diatonic(self, key: Key) -> list[NoteOctave]:
        diatonic_ = [ NoteOctave.from_notename(key.name) ]
        for n in range(len(self.interval)-1):
            note = diatonic_[n] + self.interval[n]
            notename = note.names_sequence[2]
            if notename is None:
                notename = note.names_sequence[self.policy + 2]
            diatonic_.append( NoteOctave.from_notename(notename) )
        return diatonic_

    @functools.lru_cache(maxsize=None)
    def _nondiatonic(self, key: Key) -> list[NoteOctave]:
        root = self.diatonic[0]
        diatonic_ = [ d.pitchclass - root.pitchclass for d in self.diatonic ]
        nondiatonic_ = []
        for n in range(12):
            if n in diatonic_:
                nondiatonic_.append( self.diatonic[diatonic_.index(n)] )
            else:
                note = root + n
                notename = note.names_sequence[self.policy + 2]
                if notename is None:
                    notename = note.names_sequence[2]
                nondiatonic_.append( NoteOctave.from_notename(notename) )
        return nondiatonic_



# -------------------------------------
#   Curch Modes
# -------------------------------------
class CurchMode(Scale):

    accidental: t.ClassVar[tuple[int]]

    @functools.lru_cache(maxsize=None)
    def _diatonic(self, key: Key) -> list[NoteOctave]:
        diatonic_ = [ NoteOctave.from_notename(key.name) ]
        k_mask = generate_mask_by_key(key)
        for n in range(6):
            note = diatonic_[n] + self.interval[n]
            notename = note.names_sequence[self.accidental[n+1] + k_mask[n+1] + 2]
            diatonic_.append( NoteOctave.from_notename(notename) )
        return diatonic_

class Ionian(CurchMode):
    accidental = (0,  0,  0,  0,  0,  0,  0)
    interval     = BASE_INTERVAL
class Dorian(CurchMode):
    accidental = (0,  0, -1,  0,  0,  0, -1)
    interval     = BASE_INTERVAL[1:] + BASE_INTERVAL[:1]
class Phrygian(CurchMode):
    accidental = (0, -1, -1,  0,  0, -1, -1)
    interval     = BASE_INTERVAL[2:] + BASE_INTERVAL[:2]
class Lydian(CurchMode):
    accidental = (0,  0,  0,  1,  0,  0,  0)
    interval     = BASE_INTERVAL[3:] + BASE_INTERVAL[:3]
class Mixolydian(CurchMode):
    accidental = (0,  0,  0,  0,  0,  0, -1)
    interval     = BASE_INTERVAL[4:] + BASE_INTERVAL[:4]
class Aeorian(CurchMode):
    accidental = (0,  0, -1,  0,  0, -1, -1)
    interval     = BASE_INTERVAL[5:] + BASE_INTERVAL[:5]
class Locrian(CurchMode):
    accidental = (0, -1, -1,  0, -1, -1, -1)
    interval     = BASE_INTERVAL[6:] + BASE_INTERVAL[:6]

# -------------------------------------
#   Curchmode alias
# -------------------------------------
class Major(Ionian): pass
class Minor(Aeorian): pass

# -------------------------------------
#  Curchmode derivation
# -------------------------------------
class DerivedMode(CurchMode):

    @functools.lru_cache(maxsize=None)
    def _diatonic(self, key: Key) -> list[NoteOctave]:
        k_mask = generate_mask_by_key(key)
        accidental, k_mask = _interpreted_diatonic_elements(self.accidental, k_mask)
        diatonic_ = [ NoteOctave.from_notename(key.name) ]
        for n in range(len(self.interval)-1):
            note = diatonic_[n] + self.interval[n]
            notename = note.names_sequence[accidental[n+1] + k_mask[n+1] + 2]
            diatonic_.append( NoteOctave.from_notename(notename) )
        return diatonic_

class HMajor(DerivedMode):
    name = "Harmonic Major"
    accidental = (0,  0,  0,  0,  0, -1,  0)
    interval     = (2,  2,  1,  2,  1,  3,  1)
class MMajor(DerivedMode):
    name = "Melodic Major"
    accidental = (0,  0,  0,  0,  0, -1, -1)
    interval     = (2,  2,  1,  2,  1,  2,  2)
class HMinor(DerivedMode):
    name = "Harmonic Minor"
    accidental = (0,  0, -1,  0,  0, -1,  0)
    interval     = (2,  1,  2,  2,  1,  3,  1)
class MMinor(DerivedMode):
    name = "Melodic Minor"
    accidental = (0,  0, -1,  0,  0,  0,  0)
    interval     = (2,  1,  2,  2,  2,  2,  1)
class HMinor_P5B(DerivedMode):
    name = "Harmonic Minor P5th Below"
    accidental = (0, -1,  0,  0,  0, -1, -1)
    interval     = (1,  3,  1,  2,  1,  2,  2)

# Pentatonic
class Pentatonic(DerivedMode):
    accidental = (0, 0, 0, None, 0, 0, None)
    interval     = (2, 2, 3, 2, 3)
class MinorPentatonic(DerivedMode):
    accidental = (0, None, -1, 0, 0, None, -1)
    interval     = (3,  2, 2, 3,  2)

# denature
class Ionian_s5(CurchMode):
    accidental = (0, 0, 0, 0, 1, 0, 0)
    interval     = (2, 2, 1, 3, 1, 2, 1)
class Dorian_f2(CurchMode):
    accidental = (0, -1, -1, 0, 0, 0, -1)
    interval     = (1, 2, 2, 2, 2, 1,  2)
class Dorian_s4(CurchMode):
    accidental = (0, 0, -1, 1, 0, 0, -1)
    interval     = (2, 1,  3, 1, 2, 1,  2)
class Lydian_s2(CurchMode):
    accidental = (0, 1, 0, 1, 0, 0, 0)
    interval     = (3, 1, 2, 1, 2, 2, 1)
class Lydian_s5(CurchMode):
    accidental = (0, 0, 0, 1, 1, 0, 0)
    interval     = (2, 2, 2, 2, 1, 2, 1)
class Lydian_f7(CurchMode):
    accidental = (0, 0, 0, 1, 0, 0, -1)
    interval     = (2, 2, 2, 1, 2, 1, 2)
class Mixolydian_f6(CurchMode):
    accidental = (0, 0, 0, 0, 0, -1, -1)
    interval     = (2, 2, 1, 2, 1, 2, 2)
class Aeorian_f5(CurchMode):
    accidental = (0, 0, -1, 0, -1, -1, -1)
    interval     = (2, 1, 2, 1, 2, 2, 2)
class Locrian_n6(CurchMode):
    accidental = (0, -1, -1,  0, -1, 0, -1)
    interval     = (1, 2, 2, 1, 3, 1, 2)
class Locrian_super(CurchMode):
    accidental = (0, -1, -1, -1, -1, -1, -1)
    interval     = (1, 2, 1, 2, 2, 2, 2)

# -------------------------------------
#   special Scale
# -------------------------------------
class Bluenote(Scale):
    interval = (2, 1, 1, 1, 1, 1, 2, 1, 1, 1)
class Diminish(Scale):
    interval = (2, 1, 2, 1, 2, 1, 2, 1)
class CombDiminish(Scale):
    interval = (1, 2, 1, 2, 1, 2, 1, 2)
class Wholetone(Scale):
    interval = (2, 2, 2, 2, 2, 2)



CURCH_MODES = (
    Lydian,
    Ionian,
    Mixolydian,
    Dorian,
    Aeorian,
    Phrygian,
    Locrian
)
