import configparser, pathlib
from numpy import (
    float256,
    float128,
    float64,
    float32,
    float16,
)


class Config(dict):

    def __init__(self, path, encoding="utf-8"):
        self._path = path
        self._cfg = configparser.ConfigParser()
        self._cfg.read(path, encoding)

        super().__init__()

    def update(self, path = None, encoding="utf-8"):
        if path is not None:
            self._path = path
        self._cfg.read(self._path, encoding)

    def regist(self):
        self._cfg
