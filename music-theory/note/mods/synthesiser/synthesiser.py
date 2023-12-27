from .abc import SynthesiserObject, Oscillator, Filter, Envelope, Modulator


class Synthesiser(SynthesiserObject):

    def __init__(
            self, 
            oscillator: Oscillator, 
            filter: Filter = None,
            envelope: Envelope = None,
            modulator: Modulator = None,
            ):
        
        self._osi = oscillator
        self._fil = filter
        self._env = envelope
        self._mod = modulator
    
    def wave(self, hz: float, sec: float = 1.):
        return self._osi.wave(hz, sec)