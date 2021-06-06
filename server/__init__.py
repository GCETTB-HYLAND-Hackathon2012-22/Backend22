from typing import List
from fastapi import Depends
from fastapi.responses import HTMLResponse
from .router import router
from .database import get_db, Session
from . import security, crud, models

@router.get('/api', response_class=HTMLResponse)
async def index(db: Session = Depends(get_db)):
    return 'Hello API'


@router.get('/api/doctors', response_model=List[models.Doctor])
async def get_doctors_list(db: Session = Depends(get_db), skip: int = None, limit: int = None):
    return crud.get_doctors(db, skip, limit)