import pathlib
from typing import List
from fastapi import Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .router import router
from .database import get_db, Session
from . import security, crud, models, ml_helper

@router.get('/api', response_class=HTMLResponse)
async def index(db: Session = Depends(get_db)):
    '''For Debug Purpose Only'''
    return 'Hello API'


@router.get('/api/doctors', response_model=List[models.Doctor])
async def get_doctors_list(db: Session = Depends(get_db), skip: int = None, limit: int = None):
    '''Returns the list of all doctors in a paginated format'''
    return crud.get_doctors(db, skip, limit)


@router.get('/api/vendors', response_model=List[models.Vendor])
async def get_vendors_list(db: Session = Depends(get_db), skip: int = None, limit: int = None):
    '''Returns the list of all vendors in a paginated format'''
    return crud.get_vendors(db, skip, limit)


@router.post('/api/covi_tracker')
async def predict_covid(symptoms: ml_helper.Covi_Tracker):
    return {'result': ml_helper.predict(symptoms)}