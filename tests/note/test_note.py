import pytest
from music_theory import NoteMidi, NoteOctave, MIDI_NUMBER, OCTAVE_NUMBER


@pytest.fixture
def data_octavenumbers():
    return [ n for n in range(OCTAVE_NUMBER) ]

@pytest.fixture
def data_midinumbers():
    return [ n for n in range(MIDI_NUMBER) ]

@pytest.fixture
def data_octavenotenames():
    # A~G (35types)
    from music_theory.note._statics import PITCH_TO_NOTENAME
    data = []
    for pitchclass in range(OCTAVE_NUMBER):
        data.append([ ns for ns in PITCH_TO_NOTENAME[pitchclass] if ns is not None])
    return data

@pytest.fixture
def data_midinotenames():
    # C-1 ~ G9
    from music_theory.note._statics import PITCH_TO_NOTENAME
    data = []
    for pitch in range(-1, 10):
        for pitchclass in range(OCTAVE_NUMBER):

            # notenumber is 127
            if pitch == 9 and pitchclass == 8:
                break

            names_seq = [ ns for ns in PITCH_TO_NOTENAME[pitchclass] if ns is not None]
            names = [ n + str(pitch) for n in names_seq ]

            if pitchclass == 0 and pitch == -1:
                data.append(names[:-1])
            elif pitchclass == 7 and pitch == 9:
                data.append(names[1:])
            else:
                data.append(names)

    return data

@pytest.fixture
def data_octavenotenames_sequence():
    # A~G (35types)
    from music_theory.note._statics import PITCH_TO_NOTENAME
    data = []
    for pitchclass in range(OCTAVE_NUMBER):
        data.append(PITCH_TO_NOTENAME[pitchclass])
    return data

@pytest.fixture
def data_midinotenames_sequence():
    # C-1 ~ G9
    from music_theory.note._statics import PITCH_TO_NOTENAME
    data = []
    for pitch in range(-1, 10):
        for pitchclass in range(OCTAVE_NUMBER):
            # notenumber is 127
            if pitch == 9 and pitchclass == 8:
                break
            data.append(PITCH_TO_NOTENAME[pitchclass])
    return data


class TestNoteOctave:

    def test_noteoctave_init(self, data_octavenumbers):
        for i in data_octavenumbers:
            n = NoteOctave(i)
            assert isinstance(n, NoteOctave)

    def test_noteoctave_prop_pitchclass(self, data_octavenumbers):
        for i in data_octavenumbers:
            n = NoteOctave(i)
            assert n.pitchclass == i

    def test_noteoctave_prop_name(self, data_octavenumbers):
        for i in data_octavenumbers:
            n = NoteOctave(i)
            assert n.name == None

    def test_noteoctave_prop_names(self, data_octavenumbers, data_octavenotenames):
        for i in data_octavenumbers:
            n = NoteOctave(i)
            assert n.names == data_octavenotenames[i]

    def test_noteoctave_prop_names_sequence(self, data_octavenumbers, data_octavenotenames_sequence):
        for i in data_octavenumbers:
            n = NoteOctave(i)
            assert n.names_sequence == data_octavenotenames_sequence[i]

    def test_noteoctave_eq(self, data_octavenumbers):
        for i in data_octavenumbers:
            n = NoteOctave(i)
            assert n == i

    def test_noteoctave_ne(self, data_octavenumbers):
        for i in data_octavenumbers:
            n = NoteOctave(i)
            assert not n != i

    def test_noteoctave_add(self, data_octavenumbers):
        for i in data_octavenumbers:
            for j in range(OCTAVE_NUMBER):
                n = NoteOctave(i)
                assert (n + j).pitchclass == (i + j)%OCTAVE_NUMBER

    def test_noteoctave_sub(self, data_octavenumbers):
        for i in data_octavenumbers:
            for j in range(OCTAVE_NUMBER):
                n = NoteOctave(i)
                assert (n - j).pitchclass == (i - j)%OCTAVE_NUMBER

    def test_noteoctave_int(self, data_octavenumbers):
        for i in data_octavenumbers:
            n = NoteOctave(i)
            assert int(n) == i

    def test_noteoctave_str(self, data_octavenumbers, data_octavenotenames):
        for i in data_octavenumbers:
            n = NoteOctave(i)
            assert str(n) == str(data_octavenotenames[i])

    def test_noteoctave_repr(self, data_octavenumbers, data_octavenotenames):
        for i in data_octavenumbers:
            n = NoteOctave(i)
            assert repr(n) == repr(data_octavenotenames[i])

    def test_noteoctave_is_pitchclass(self, data_octavenumbers):
        for i in data_octavenumbers:
            assert NoteOctave.is_pitchclass(i)

    def test_noteoctave_is_notename(self, data_octavenumbers):
        for i in data_octavenumbers:
            assert not NoteOctave.is_notename(i)


class TestNoteOctave_from_notename:

    def test_noteoctave_from_notename(self, data_octavenotenames):
        for names in data_octavenotenames:
            for name in names:
                n = NoteOctave.from_notename(name)
                assert isinstance(n, NoteOctave)

    def test_noteoctave_prop_name(self, data_octavenotenames):
        for names in data_octavenotenames:
            for name in names:
                n = NoteOctave.from_notename(name)
                assert n.name == name

    def test_noteoctave_str(self, data_octavenotenames):
        for names in data_octavenotenames:
            for name in names:
                n = NoteOctave.from_notename(name)
                assert str(n) == name

    def test_noteoctave_repr(self, data_octavenotenames):
        for names in data_octavenotenames:
            for name in names:
                n = NoteOctave.from_notename(name)
                assert repr(n) == name


class TestNoteMidi:

    def test_notemidi_init(self, data_midinumbers):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert isinstance(n, NoteMidi)

    def test_notemidi_prop_number(self, data_midinumbers):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert n.number == i

    def test_notemidi_prop_pitch(self, data_midinumbers):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert n.pitch == (i//OCTAVE_NUMBER - 1)

    def test_notemidi_prop_pitchclass(self, data_midinumbers):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert n.pitchclass == i%OCTAVE_NUMBER

    def test_notemidi_prop_name(self, data_midinumbers):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert n.name == None

    def test_notemidi_prop_names(self, data_midinumbers, data_midinotenames):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert n.names == data_midinotenames[i]

    def test_notemidi_prop_names_sequence(self, data_midinumbers, data_midinotenames_sequence):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert n.names_sequence == data_midinotenames_sequence[i]

    def test_notemidi_eq(self, data_midinumbers):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert n == i

    def test_notemidi_ne(self, data_midinumbers):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert not n != i

    def test_notemidi_lt(self, data_midinumbers):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert not n < i

    def test_notemidi_gt(self, data_midinumbers):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert not n > i

    def test_notemidi_le(self, data_midinumbers):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert n <= i

    def test_notemidi_ge(self, data_midinumbers):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert n >= i

    def test_notemidi_add(self, data_midinumbers):
        for i in data_midinumbers:
            for j in data_midinumbers[:-i]:
                n = NoteMidi(i)
                assert (n + j).number == i + j

    def test_notemidi_sub(self, data_midinumbers):
        for i in data_midinumbers:
            for j in data_midinumbers[:i]:
                n = NoteMidi(i)
                assert (n - j).number == i - j

    def test_notemidi_matmul(self, data_midinumbers):
        for i in data_midinumbers:
            upper_lim = (len(data_midinumbers)-1 - i) // OCTAVE_NUMBER
            lower_lim = i // OCTAVE_NUMBER
            for j in range(lower_lim, upper_lim):
                n = NoteMidi(i)
                assert (n @ j).number == i + OCTAVE_NUMBER*j

    def test_notemidi_int(self, data_midinumbers):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert int(n) == i

    def test_notemidi_str(self, data_midinumbers, data_midinotenames):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert str(n) == f"<NoteMidi: {data_midinotenames[i]}; number: {i}>"

    def test_notemidi_repr(self, data_midinumbers, data_midinotenames):
        for i in data_midinumbers:
            n = NoteMidi(i)
            assert repr(n) == f"<NoteMidi: {data_midinotenames[i]}; number: {i}>"

    def test_notemidi_is_pitchclass(self, data_octavenumbers):
        for i in data_octavenumbers:
            assert NoteMidi.is_pitchclass(i)

    def test_notemidi_is_notenumber(self, data_midinumbers):
        for i in data_midinumbers:
            assert NoteMidi.is_notenumber(i)

    def test_notemidi_is_notename(self, data_midinotenames):
        for names in data_midinotenames:
            for name in names:
                assert NoteMidi.is_notename(name)


class TestNoteMidi_from_notename:

    def test_notemidi_from_notename(self, data_midinotenames):
        for names in data_midinotenames:
            for name in names:
                n = NoteMidi.from_notename(name)
                assert isinstance(n, NoteMidi)

    def test_notemidi_prop_name(self, data_midinotenames):
        for names in data_midinotenames:
            for name in names:
                n = NoteMidi.from_notename(name)
                assert n.name == name

    def test_notemidi_str(self, data_midinotenames):
        for i, names in enumerate(data_midinotenames):
            for name in names:
                n = NoteMidi.from_notename(name)
                assert str(n) == f"<NoteMidi: {name}; number: {i}>"

    def test_notemidi_repr(self, data_midinotenames):
        for i, names in enumerate(data_midinotenames):
            for name in names:
                n = NoteMidi.from_notename(name)
                assert repr(n) == f"<NoteMidi: {name}; number: {i}>"
