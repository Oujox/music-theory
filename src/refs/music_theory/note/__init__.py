"""
Note
====

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
"""

from .note import NoteMidi
from .note import NoteOctave
from .note import MIDI_NUMBER
from .note import OCTAVE_NUMBER

from .key import Key, ALL_KEYNAME
from . import scale
from . import tuner

__all__ = [
    "NoteMidi",
    "NoteOctave",
    "Key",
    "scale",
    "tuner"
]
