"""
NotePy
======

Provides
  1. Name of note, characteristics, playback
  2. Relationship of notes within a scale

How to use the documentation
----------------------------
Docstrings provided with the code
  
  >>> import note
  >>> help(note.Note) 

Available subpackages
---------------------
tuner
    Provide frequencies that vary with the
    method of sound tuning
synth
    Provides an array of waveforms for changing tones
"""

from .note import Note, NoteSimple
from .key import Key, NoteBase
from . import scale

from .handlers import (
    TunerHandler, SynthesiserHandler, NoteHandlerProxy)

from .mods import tuner
from .mods import synthesiser as synthe

