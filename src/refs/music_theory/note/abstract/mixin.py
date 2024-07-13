
import typing as t
from .base import BaseScale
from ..config import ConfigContext, Config


class MixinConfig:
    def __init__(self, *args, **kwargs):
        self.config: t.Optional[ConfigContext] = kwargs.pop('scale', Config)
        super(MixinConfig, self).__init__()


class MixinScale:
    def __init__(self, *args, **kwargs):
        self.scale: t.Optional[BaseScale] = kwargs.pop('scale', None)
        super(MixinScale, self).__init__()

    def __call__(self, scale: BaseScale) -> t.Self:
        self.scale = scale
        return self
