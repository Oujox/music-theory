import numpy as _np
import scipy.signal as _sg

from .abc import OscillatorBase


class Sinewave(OscillatorBase):

    def wave(self, hz: float, sec: float = 1.) -> _np.ndarray:
        t = _np.arange(0, self.sampling_hz*sec)
        return _np.sin(2 * _np.pi * hz * t / self.sampling_hz)

class Suqarewave(OscillatorBase):

    def wave(self, hz: float, sec: float = 1.) -> _np.ndarray:
        t = _np.arange(0, self.sampling_hz*sec)
        return _sg.square(2 * _np.pi * hz * t / self.sampling_hz)

class Sawtoothwave(OscillatorBase):

    def wave(self, hz: float, sec: float = 1.) -> _np.ndarray:
        t = _np.arange(0, self.sampling_hz*sec)
        return _sg.sawtooth(2 * _np.pi * hz * t / self.sampling_hz) 

class Trianglewave(OscillatorBase):

    def wave(self, hz: float, sec: float = 1.) -> _np.ndarray:
        t = _np.arange(0, self.sampling_hz*sec)
        return _sg.sawtooth(2 * _np.pi * hz * t / self.sampling_hz, 0.5)

class Noisewave(OscillatorBase):

    def wave(self, hz: float, sec: float = 1.) -> _np.ndarray:
        return _np.random.normal(0, 1, int(self.sampling_hz*sec))