
import typing as t
import os, copy
import pathlib, tomllib
from contextvars import ContextVar, Token
from contextlib import ContextDecorator

from ..utils import SingletonMeta





class ConfigMT(t.Mapping, metaclass=SingletonMeta):

    type Mode = t.Literal["all", "inc", "diff"]
    type Type = dict[str, int|str|ConfigMT]

    __config: ContextVar[Type]
    __token: Token[Type]

    def __init__(self) -> None:
        self.__config = ContextVar("config")

    def load(self, file: pathlib.Path|Type, mode: Mode = "diff") -> t.Self:
        if isinstance(file, (str, pathlib.Path)):
            path = pathlib.Path(file)
            config = tomllib.load(open(path, mode="rb"))
        elif isinstance(file, dict):
            config = file
        self.__update(config, mode)
        return self

    def __update(self, config: Type, mode: Mode) -> t.Self:
        if mode == "all":
            self.__token = self.__config.set(config)
        if mode == "inc":
            _config = copy.deepcopy(self.__config.get())
            _ = [ _config.setdefault(k, v) for (k, v) in config.items() ]
            self.__token = self.__config.set(_config)
        if mode == "diff":
            _config = copy.deepcopy(self.__config.get())
            _config.update(config)
            self.__token = self.__config.set(_config)
        return self

    def __getitem__(self, key: str) -> t.Any:
        return self._config.get().__getitem__(key)

    def __iter__(self) -> t.Iterator[str]:
        return self._config.get().__iter__()

    def __len__(self) -> int:
        return self._config.get().__len__()


class ContextMT(ContextDecorator, t.Mapping):

    _config: t.ClassVar[ContextVar[dict[str, t.Any]]] = ContextVar("config")

    def __init__(self, filepath_or_dict: str|pathlib.Path|dict[str, t.Any]) -> None:
        self._config = ContextVar("config")
        self.load(filepath_or_dict, mode="all")

    @property
    def config(self):
        return self._config.get()

    def load(self, filepath_or_dict: str|pathlib.Path|dict[str, t.Any], mode: t.Literal["all", "inc", "diff"] = "diff") -> t.Self:
        if isinstance(filepath_or_dict, (str, pathlib.Path)):
            path = pathlib.Path(filepath_or_dict)
            config = tomllib.load(open(path, mode="rb"))
        elif isinstance(filepath_or_dict, dict):
            config = filepath_or_dict
        else:
            raise ValueError("The argument filepath_or_dict must be str, pathlib.Path or dict.")

        self.__update(config, mode)
        return self

    def __update(self, config: dict[str, t.Any], mode: t.Literal["all", "inc", "diff"]) -> t.Self:
        if mode == "all":
            self.__token = self._config.set(config)
        if mode == "inc":
            _config = copy.deepcopy(self._config.get())
            _ = [ _config.setdefault(k, v) for (k, v) in config.items() ]
            self.__token = self._config.set(_config)
        if mode == "diff":
            _config = copy.deepcopy(self._config.get())
            _config.update(config)
            self.__token = self._config.set(_config)
        return self

    def __enter__(self) -> t.Self:
        return self

    def __exit__(self, *tracebacks):
        self._config.reset(self.__token)

    def __getitem__(self, key: str) -> t.Any:
        return self._config.get().__getitem__(key)

    def __iter__(self) -> t.Iterator[str]:
        return self._config.get().__iter__()

    def __len__(self) -> int:
        return self._config.get().__len__()




config_paths = [
    pathlib.Path().cwd() / "config.toml",
    pathlib.Path(os.path.dirname(__file__)) / "config.toml"
]

def reload() -> ContextMT:
    for path in config_paths:
        try:
            return ContextMT(path)
        except FileNotFoundError as e:
            pass
        except Exception as e:
            raise Exception("unexpected error. [{}]".format(e))

    return ContextMT({})

Config = reload()
