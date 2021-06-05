from fastapi import Depends
from fastapi.responses import HTMLResponse
from .router import router
from .database import get_db, Session

@router.get('/', response_class=HTMLResponse)
async def index(db: Session = Depends(get_db)):
    return 'Hello World'