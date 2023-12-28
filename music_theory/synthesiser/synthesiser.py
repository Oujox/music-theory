from .abc import SynthesiserObject, Oscillator, Filter, Envelope, Modulator


class Synthesiser(SynthesiserObject):

    def __init__(
            self,
            oscillator: Oscillator,
            filter: Filter = None,
            envelope: Envelope = None,
            modulator: Modulator = None,
            ):

        self.osi = oscillator
        self.fil = filter
        self.env = envelope
        self.mod = modulator

    def wave(self, hz: float, sec: float = 1.):
        return self.osi.wave(hz, sec)