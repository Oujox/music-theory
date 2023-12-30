from .abc import ToneBase, OscillatorBase, FilterBase, EnvelopeBase, ModulatorBase
import os, datetime, wave, pyaudio, atexit
import numpy as np

AudioPort = pyaudio.PyAudio()
atexit.register(lambda : AudioPort.terminate())


class Synthesiser(ToneBase):

    def __init__(
            self,
            oscillator : OscillatorBase,
            filter     : FilterBase = None,
            envelope   : EnvelopeBase = None,
            modulator  : ModulatorBase = None,
            ):

        self.osi = oscillator
        self.fil = filter
        self.env = envelope
        self.mod = modulator

    def wave(self, hz: float, sec: float = 1.):
        return self.osi.wave(hz, sec)

    def play(self, wave_: np.ndarray) -> None:
        wave_ = wave_ * ((2**15)-1 / np.max(wave_))
        bin_wave = wave_.astype(np.int16).tobytes()

        stream_out = AudioPort.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.osi.sampling_hz,
            frames_per_buffer=1024,
            input=False,
            output=True,
            )
        try:
            while stream_out.is_active():
                stream_out.write(bin_wave)
        except KeyboardInterrupt:
            pass
        stream_out.stop_stream()
        stream_out.close()

    def save(self, path: str, wave_: np.ndarray, hz: float) -> str:
        now = datetime.datetime.now().strftime(f"%Y%m%d-%H%M%S")
        path = os.path.join(path, "{}_{}hz_{}.wav".format(self.__class__.__name__, int(hz), now))

        wave_ = wave_ * ((2**15)-1 / np.max(wave_))
        binary_wave = wave_.astype(np.int16).tobytes()

        file = wave.open(path, mode="wb")
        param = (1, 2, self.osi.sampling_hz, len(binary_wave), 'NONE', 'not compressed')
        file.setparams(param)
        file.writeframes(binary_wave)
        file.close()
        return path
