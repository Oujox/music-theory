from .key import Key
from .abc import Scale
from ._const import FIFTH_SEQUENCE


def count_flat_sharp(key: Key) -> int:
    fs_count = FIFTH_SEQUENCE.index(key.pitchclass)
    if key.pitchclass == 6:
        # TODO: key._pos is eq to 2 or 3
        fs_count = fs_count - 12 if fs_count > int(key._pos == 3) + 5 else fs_count
    else:
        fs_count = fs_count - 12 if fs_count > 5 else fs_count
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
    def diatonic(self):
        diatonic_ = [ self.key ]
        
        fs_count = count_flat_sharp(self.key)
        k_mask = generate_mask_by_key(fs_count)

        for n in range(6):
            diatonic_.append(diatonic_[n].next(self.degree[n], self.s_mask[n+1] + k_mask[n+1]))
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