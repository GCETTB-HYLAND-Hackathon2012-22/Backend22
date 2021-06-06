import uvicorn
from .environ import Config

# START SERVER
# -------------
# If localhost, port is not required to be explicitely mentioned

if Config.isLocal:
    uvicorn.run('server:router', reload=True)
else:
    uvicorn.run('server:router', host='0.0.0.0', port=int(Config.PORT))