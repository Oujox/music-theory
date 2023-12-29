from music_theory import NoteMidi, synthe, tuner, scale

c = NoteMidi(84, tuner=tuner.EqualTemperament(440), synthe=synthe.Synthesiser(synthe.osi.Sinewave()))
print(scale.Locrian("C").diatonic)
