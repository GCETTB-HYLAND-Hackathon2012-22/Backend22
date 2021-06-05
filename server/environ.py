import pathlib
from typing import Any
from starlette.config import Config

class CustomConfig(Config):
    def __getattr__(self, name: str) -> Any:
        return self.get(name, default=None)
    
    @property
    def isLocal(self) -> bool:
        return Config.PORT is None;

Config = CustomConfig(pathlib.Path(__file__).parent.parent / '.env')

del CustomConfig

__all__ = ['Config']

if __name__ == '__main__':
    if Config.isLocal:
        print('Running on Local Machine')
    else:
        print('Running on Cloud Server')