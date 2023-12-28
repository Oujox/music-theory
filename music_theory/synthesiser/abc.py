import os, datetime, wave, pyaudio
from abc import ABCMeta, abstractmethod
import numpy as np

from ..note import NoteMod


class Oscillator(metaclass=ABCMeta):

    def __init__(self, sampling_hz: int = 44100) -> None:
        self._sampling_hz = sampling_hz

    @abstractmethod
    def wave(self, hz: float, sec: float) -> np.ndarray:
        pass


class Filter(metaclass=ABCMeta):
    pass


class Envelope(metaclass=ABCMeta):
    pass


class Modulator(metaclass=ABCMeta):
    pass


class SynthesiserObject(NoteMod, metaclass=ABCMeta):

    osi: Oscillator
    fil: Filter
    env: Envelope
    mod: Modulator

    @abstractmethod
    def wave(self, sec: float) -> np.ndarray:
        pass

    def sound(self, wave_: np.ndarray) -> None:
        p = pyaudio.PyAudio()
        wave_ = wave_ * ((2**15)-1 / np.max(wave_))
        bin_wave = wave_.astype(np.int16).tobytes()

        stream_out = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.osi._sampling_hz,
            frames_per_buffer=1024,
            input=False,
            output=True,
            )

        while stream_out.is_active():
            stream_out.write(bin_wave)
        stream_out.stop_stream()
        stream_out.close()
        p.terminate()

    def save(self, path: str, wave_: np.ndarray, hz: float) -> str:
        now = datetime.datetime.now().strftime(f"%Y%m%d-%H%M%S")
        path = os.path.join(path, "{}_{}hz_{}.wav".format(self.__class__.__name__, int(hz), now))

        wave_ = wave_ * ((2**15)-1 / np.max(wave_))
        binary_wave = wave_.astype(np.int16).tobytes()

        file = wave.open(path, mode="wb")
        param = (1, 2, self.osi._sampling_hz, len(binary_wave), 'NONE', 'not compressed')
        file.setparams(param)
        file.writeframes(binary_wave)
        file.close()
        return path


