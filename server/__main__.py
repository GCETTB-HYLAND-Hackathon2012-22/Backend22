import uvicorn
from .environ import Config

if Config.isLocal:
    uvicorn.run('server:router')
else:
    uvicorn.run('server:router', host='0.0.0.0', port=int(Config.PORT))