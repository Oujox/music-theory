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
synth
    Provides an array of waveforms for changing tones
"""

from .note import Note, NoteBase
from .key import Key
from . import scale

from .mod import NoteMod
from .handler import NoteHandlerProxy
