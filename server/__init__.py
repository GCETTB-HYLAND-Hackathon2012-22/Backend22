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
        key=lambda x: geolocation.distance_or_Inf(lat, long, x.user_obj.latitude, x.user_obj.longitude)
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
        key=lambda x: geolocation.distance_or_Inf(lat, long, x.user_obj.latitude, x.user_obj.longitude)
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


@router.get('/api/oxygen', response_model=List[models.VendorProduct])
async def get_oxygen_list(db: Session = Depends(get_db), lat: int=None, long: int=None):
    return sorted(crud.get_oxygen(db),
        key=lambda x: geolocation.distance_or_Inf(lat, long, x.vendor_obj.user_obj.latitude, x.vendor_obj.longitude)
    )


@router.get('/api/medicine', response_model=List[models.VendorProduct])
async def get_medicine_list(db: Session = Depends(get_db), lat: int=None, long: int=None):
    return sorted(crud.get_medicine(db),
        key=lambda x: geolocation.distance_or_Inf(lat, long, x.vendor_obj.user_obj.latitude, x.vendor_obj.longitude)
    )


@router.post('/api/appointment', response_model=models.AppointmentListForUser)
async def set_appointment(appointment: models.AppointmentListForUser, db: Session = Depends(get_db)):
    return crud.set_appointment(db, appointment)


# MEDI-CHECKER

@router.post('/api/medi_checker')
async def predict_health(symptoms: ml_helper.Medi_Checker):
    return {'Covid': ml_helper.predict(symptoms)}


@router.post('/api/medi_checker/from_xray')
async def predict_health_from_image(file: UploadFile = File(...)):
    result = await dl_helper.predict(file)
    return {dl_helper.class_list[i]: float(result[i]) for i in range(len(dl_helper.class_list)) if dl_helper.class_list[i] not in dl_helper.ext_class}