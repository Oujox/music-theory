
from music_theory import *

c = Note(84, tuner=tuner.EqualTemperament(440), synthe=synthe.Synthesiser(synthe.osi.Sinewave()))
c._wave(sound=True)
