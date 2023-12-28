from .synthesiser import SynthesiserHandler


class Note_(SynthesiserHandler):
    """
    Data to provide many ways of expressing things about note

    Parameters
    ----------
    note_number : int
        note_number in midi standard
    tuner : TunerObject
        Tuner object provided by ``note.tuner``
    synthe : SynthesiserObject
        Synthesiser object provided by ``note.synthe``

    See Also
    --------
    Note.from_notename : Constructor from notename and pitch.

    Examples
    --------
    Constructing Note from a note_number.

      >>> n_num = 60  # is Dbb4, C4 or B#4
      >>> c4 = Note(note_number=n_num)
      >>> c4
      <Note: ['Dbb4', 'C4', 'B#4']; number: 60>

    Constructing Note from a notename.

      >>> n_name, n_pitch = "C", 4
      >>> c4 = Note.from_notename(name=n_name, picth=n_pitch)
      >>> c4

      >>> <Note: C4; number: 60>

    """
    def __init__(self, note_number: int, **kwargs) -> None:
        super().__init__(note_number, **kwargs)