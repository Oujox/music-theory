import numpy as _np
import scipy.signal as _sg

from .abc import Oscillator


class Sinewave(Oscillator):
    
    def wave(self, hz: float, sec: float = 1.) -> _np.ndarray:
        t = _np.arange(0, self._sampling_hz*sec)
        return _np.sin(2 * _np.pi * hz * t / self._sampling_hz)
    
class Suqarewave(Oscillator):

    def wave(self, hz: float, sec: float = 1.) -> _np.ndarray:
        t = _np.arange(0, self._sampling_hz*sec)
        return _sg.square(2 * _np.pi * hz * t / self._sampling_hz)
    
class Sawtoothwave(Oscillator):

    def wave(self, hz: float, sec: float = 1.) -> _np.ndarray:
        t = _np.arange(0, self._sampling_hz*sec)
        return _sg.sawtooth(2 * _np.pi * hz * t / self._sampling_hz) 

class Trianglewave(Oscillator):

    def wave(self, hz: float, sec: float = 1.) -> _np.ndarray:
        t = _np.arange(0, self._sampling_hz*sec)
        return _sg.sawtooth(2 * _np.pi * hz * t / self._sampling_hz, 0.5)
    
class Noisewave(Oscillator):

    def wave(self, hz: float, sec: float = 1.) -> _np.ndarray:
        return _np.random.normal(0, 1, int(self._sampling_hz*sec))