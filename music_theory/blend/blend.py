import pyaudio
import numpy as np

from .abc import BlendBase
from ..note.abc import TunerBase
from ..note_derived import Note


class Blend(BlendBase):

    def __init__(
            self,
            *note: Note,
            sampling_hz: int = 44100,
            tuner: TunerBase|None = None,
            **kwargs
        ):

        self._notes = note
        self._tuner = tuner
        self.sampling_hz = sampling_hz

        for _note in self._notes:
            _note.tone.osi.sampling_hz = sampling_hz

    def wave(self, sec: float) -> np.ndarray:
        wave = np.zeros(int(self.sampling_hz*sec))
        for note in self._notes:
            wave += note.wave(sec)
        return wave

    def play(self, sec: float) -> np.ndarray:

        def min_max(x: np.ndarray, axis=None) -> np.ndarray:
            min = x.min(axis=axis, keepdims=True)
            max = x.max(axis=axis, keepdims=True)
            result = 2*(x-min)/(max-min) - 1
            return result

        wave = min_max(self.wave(sec))
        wave = wave * ((2**15)-1 / np.max(wave))
        bin_wave = wave.astype(np.int16).tobytes()

        p = pyaudio.PyAudio()
        stream_out = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sampling_hz,
            frames_per_buffer=1024,
            input=False,
            output=True,
            )

        while stream_out.is_active():
            stream_out.write(bin_wave)
        stream_out.stop_stream()
        stream_out.close()

        return wave

    def save(self, path: str) -> str:
        return