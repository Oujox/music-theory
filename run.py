from music_theory import Note, synthe, tuner, scale

c = Note(84, tuner=tuner.EqualTemperament(440), synthe=synthe.Synthesiser(synthe.osi.Sinewave()))
print(scale.Locrian("C").diatonic)
