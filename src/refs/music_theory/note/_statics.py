
class NoteRelations:

    base_intervals = ()
    notename_symbols = ()
    notepitch_symbols = ()

    def __init__(self) -> None:
        pass


PITCH_TO_NOTENAME: dict[int, tuple[str|None, ...]] = {
    9 : ( "Bbb" , None , "A"  , None , "G##" ),
    10: ( "Cbb" , "Bb" , None , "A#" , None  ),
    11: ( None  , "Cb" , "B"  , None , "A##" ),
    0 : ( "Dbb" , None , "C"  , "B#" , None  ),
    1 : ( None  , "Db" , None , "C#" , "B##" ),
    2 : ( "Ebb" , None , "D"  , None , "C##" ),
    3 : ( "Fbb" , "Eb" , None , "D#" , None  ),
    4 : ( None  , "Fb" , "E"  , None , "D##" ),
    5 : ( "Gbb" , None , "F"  , "E#" , None  ),
    6 : ( None  , "Gb" , None , "F#" , "E##" ),
    7 : ( "Abb" , None , "G"  , None , "F##" ),
    8 : ( None  , "Ab" , None , "G#" , None  )
}

NOTENAME_TO_PITCH: dict[str, int] = {
    "Abb": 7,  "Ab": 8,  "A" : 9,  "A#": 10, "A##": 11,
    "Bbb": 9,  "Bb": 10, "B" : 11, "B#": 0,  "B##": 1,
    "Cbb": 10, "Cb": 11, "C" : 0,  "C#": 1,  "C##": 2,
    "Dbb": 0,  "Db": 1,  "D" : 2,  "D#": 3,  "D##": 4,
    "Ebb": 2,  "Eb": 3,  "E" : 4,  "E#": 5,  "E##": 6,
    "Fbb": 3,  "Fb": 4,  "F" : 5,  "F#": 6,  "F##": 7,
    "Gbb": 5,  "Gb": 6,  "G" : 7,  "G#": 8,  "G##": 9
}

CODETONE_SYMBOLS = (
    "P1", "m2", "M2", "m3", "M3", "P4", "b5", "P5", "m6", "M6", "m7", "M7"
)

FIGURED_SYMBOLS = (
    "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ"
)

ALL_NOTENAME = tuple(NOTENAME_TO_PITCH.keys())
ALL_PITCH    = tuple(PITCH_TO_NOTENAME.keys())
ALL_KEYNAME  = tuple([ n for n in ALL_NOTENAME if len(n) < 3])

BASE_INTERVAL    = (2, 2, 1, 2, 2, 2, 1)
FIFTH_SEQUENCE = (0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5)
