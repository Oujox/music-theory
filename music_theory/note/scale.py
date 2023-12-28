from .abc import Scale
from .key import Key
from .note import NoteBase


def count_flat_sharp(key: Key) -> int:
    if key.fifth == 6:
        fs_count = fs_count - 12 if key.fifth > int(key.accsidental == 1) + 5 else key.fifth
    else:
        fs_count = fs_count - 12 if key.fifth > 5 else key.fifth
    return fs_count

def generate_mask_by_key(fs_count: int) -> list[int]:
    mask = [0]*7
    if fs_count > 0:
        for i in range(0, fs_count):
            mask[-((i*4)%7+1)] = 1
    elif fs_count < 0:
        for i in range(1, -fs_count+1):
            mask[(i*4)%7-1] = -1
    return mask


class CurchMode(Scale):

    degree: tuple[int]
    s_mask: tuple[int]

    @property
    def diatonic(self) -> list[NoteBase]:
        diatonic_ = [ NoteBase.from_notename(self.key.name) ]

        fs_count = count_flat_sharp(self.key)
        k_mask = generate_mask_by_key(fs_count)

        for n in range(6):
            note = diatonic_[n] + self.degree[n]
            notename = note.names_sequence[self.s_mask[n+1] + k_mask[n+1] + 2]
            diatonic_.append(NoteBase.from_notename(notename))

        return diatonic_


class Ionian(CurchMode):
    degree = (2,  2,  1,  2,  2,  2,  1)
    s_mask = (0,  0,  0,  0,  0,  0,  0)
class Dorian(CurchMode):
    degree = (2,  1,  2,  2,  2,  1,  2)
    s_mask = (0,  0, -1,  0,  0,  0, -1)
class Phrygian(CurchMode):
    degree = (1,  2,  2,  2,  1,  2,  2)
    s_mask = (0, -1, -1,  0,  0, -1, -1)
class Lydian(CurchMode):
    degree = (2,  2,  2,  1,  2,  2,  1)
    s_mask = (0,  0,  0,  1,  0,  0,  0)
class Mixolydian(CurchMode):
    degree = (2,  2,  1,  2,  2,  1,  2)
    s_mask = (0,  0,  0,  0,  0,  0, -1)
class Aeorian(CurchMode):
    degree = (2,  1,  2,  2,  1,  2,  2)
    s_mask = (0,  0, -1,  0,  0, -1, -1)
class Locrian(CurchMode):
    degree = (1,  2,  2,  1,  2,  2,  2)
    s_mask = (0, -1, -1,  0, -1, -1, -1)


class Major(Ionian): pass

class Minor(Aeorian): pass
