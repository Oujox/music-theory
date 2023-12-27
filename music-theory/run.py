from note import *
from chord import *

c = Note(60, tuner=tuner.EqualTemperament(442), synthe=synthe.Synthesiser(synthe.osi.Sinewave()))
c.wave(sec=5, path=".")

