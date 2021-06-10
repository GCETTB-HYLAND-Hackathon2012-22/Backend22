from typing import List
from fastapi import Depends, UploadFile, File, HTTPException, status
from fastapi.responses import HTMLResponse
from .router import router
from .database import get_db, Session
from . import security, crud, models, ml_helper, dl_helper, geolocation

@router.get('/api', response_class=HTMLResponse)
async def index(db: Session = Depends(get_db)):
    '''For Debug Purpose Only'''
    return 'Hello API'


@router.get('/api/doctors', response_model=List[models.Doctor])
async def get_doctors_list(db: Session = Depends(get_db), lat: int=None, long: int=None):
    '''Returns the list of all doctors'''
    return sorted(crud.get_doctors(db),
        key=lambda loc: geolocation.distance_or_Inf(lat, long, loc.user_obj.latitude, loc.user_obj.longitude)
    )


@router.get('/api/doctor/{uid}', response_model=models.Doctor)
async def get_doctor_by_uid(uid: str, db: Session = Depends(get_db)):
    '''Returns the doctor with the following uid'''
    res = crud.get_doctor(db, uid)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No doctor found with given uid'
        )
    return res


@router.get('/api/vendors', response_model=List[models.Vendor])
async def get_vendors_list(db: Session = Depends(get_db), lat: int=None, long: int=None):
    '''Returns the list of all vendors in a paginated format'''
    return sorted(crud.get_vendors(db),
        key=lambda loc: geolocation.distance_or_Inf(lat, long, loc.user_obj.latitude, loc.user_obj.longitude)
    )


@router.get('/api/vendor/{uid}', response_model=models.Vendor)
async def get_vendor_by_uid(uid: str, db: Session = Depends(get_db)):
    '''Returns the vendor with the following uid'''
    res = crud.get_vendor(db, uid)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No vendor found with given uid'
        )
    return res


# MEDI-CHECKER

@router.post('/api/medi_checker')
async def predict_covid(symptoms: ml_helper.Medi_Checker):
    return {'Covid': ml_helper.predict(symptoms)}


@router.post('/api/medi_checker/from_xray')
async def predict_covid_from_image(file: UploadFile = File(...)):
    result = await dl_helper.predict(file)
    return {dl_helper.class_list[i]: float(result[i]) for i in range(len(dl_helper.class_list))}