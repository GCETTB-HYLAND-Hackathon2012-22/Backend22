from fastapi.responses import HTMLResponse
from .router import router

@router.get('/', response_class=HTMLResponse)
def index():
    return 'Hello World'