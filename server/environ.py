import pathlib
from typing import Any
from starlette.config import Config

class CustomConfig(Config):
    def __getattr__(self, name: str) -> Any:
        return self.get(name, default=None)
    
    @property
    def isLocal(self) -> bool:
        '''To check weather the server is running on heroku like environment or in localhost'''
        return Config.PORT is None;

# Config object to any environment variable easily. Also works with .env files
Config = CustomConfig(pathlib.Path(__file__).parent.parent / '.env')

del CustomConfig

__all__ = ['Config']


# DEBUG

if __name__ == '__main__':
    if Config.isLocal:
        print('Running on Local Machine')
    else:
        print('Running on Cloud Server')