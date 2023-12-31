import pyaudio
import numpy as np

from .abc import MixerBase
from ..note.abc import TunerBase

from ..derived import Note
from ..audio import AudioPort
from ..utils import min_max


class Mixer(MixerBase):

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
            if tuner is not None:
                _note.tuner = tuner
            _note.tone.osi.sampling_hz = sampling_hz

    def wave(self, sec: float) -> np.ndarray:
        wave_ = np.zeros(int(self.sampling_hz*sec))
        for note in self._notes:
            wave_ += note.wave(sec)
        return wave_

    def play(self, sec: float) -> np.ndarray:

        wave_ = min_max(self.wave(sec))
        wave_ = wave_ * ((2**15)-1 / np.max(wave_))
        bin_wave = wave_.astype(np.int16).tobytes()

        stream_out = AudioPort.open(
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

        return wave_

    def save(self, path: str) -> str:
        return