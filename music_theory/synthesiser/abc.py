from abc import ABCMeta, abstractmethod
import os, datetime, wave, pyaudio
import numpy as np

from ..mst_object import MstModObject


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


class SynthesiserObject(MstModObject, metaclass=ABCMeta):

    amp = pyaudio.PyAudio()
    osi: Oscillator
    fil: Filter
    env: Envelope
    mod: Modulator

    def __del__(self) -> None:
        self.amp.terminate()

    @abstractmethod
    def wave(self, sec: float) -> np.ndarray:
        pass

    def sound(self, wave_: np.ndarray) -> None:
        wave_ = wave_ * ((2**15)-1 / np.max(wave_))
        bin_wave = wave_.astype(np.int16).tobytes()

        stream_out = self.amp.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.osi._sampling_hz,
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
        param = (1, 2, self.osi._sampling_hz, len(binary_wave), 'NONE', 'not compressed')
        file.setparams(param)
        file.writeframes(binary_wave)
        file.close()
        return path


