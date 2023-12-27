from note import *
from numpy import sum
from pandas import DataFrame


c = Note(60, tuner=tuner.EqualTemperament(440), synthe=synthe.Synthesiser(synthe.osi.Noisewave()))
print(c)
