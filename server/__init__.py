from typing import List, Union, Optional
from fastapi import Depends, UploadFile, File, HTTPException, status
from fastapi.responses import HTMLResponse
from .router import router
from .database import get_db, Session
from . import security, crud, models, ml_helper, dl_helper, geolocation, chatbot_helper

@router.get('/api', response_class=HTMLResponse)
async def index(db: Session = Depends(get_db)):
    '''For Debug Purpose Only'''
    return 'Hello API'


@router.get('/api/doctors', response_model=List[models.Doctor])
async def get_doctors_list(db: Session = Depends(get_db), lat: float=None, long: float=None):
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
async def get_vendors_list(db: Session = Depends(get_db), lat: float=None, long: float=None):
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
async def get_oxygen_list(db: Session = Depends(get_db), lat: float=None, long: float=None):
    return sorted(crud.get_oxygen(db),
        key=lambda x: geolocation.distance_or_Inf(lat, long, x.vendor_obj.user_obj.latitude, x.vendor_obj.user_obj.longitude)
    )


@router.get('/api/medicine', response_model=List[models.VendorProduct])
async def get_medicine_list(db: Session = Depends(get_db), lat: float=None, long: float=None):
    return sorted(crud.get_medicine(db),
        key=lambda x: geolocation.distance_or_Inf(lat, long, x.vendor_obj.user_obj.latitude, x.vendor_obj.user_obj.longitude)
    )


@router.post('/api/appointment', response_model=models.AppointmentListForUser)
async def set_appointment(appointment: models.AppointmentListForUser, db: Session = Depends(get_db)):
    return crud.set_appointment(db, appointment)


@router.post('/api/order/oxygen', response_model=models.UserOxygen)
async def book_oxygen(item: models.UserOxygenBase, db: Session = Depends(get_db)):
    return crud.book_oxygen(item, db)


@router.post('/api/order/medicine', response_model=models.UserMedicine)
async def book_medicine(item: models.UserMedicineBase, db: Session = Depends(get_db)):
    return crud.book_medicine(item, db)


# Chat-bot

@router.post('/api/chatbot')
async def get_chatbot_reply(question: str):
    return {'reply': chatbot_helper.robot(question)}


# MEDI-CHECKER

@router.post('/api/medi_checker')
async def predict_health(symptoms: ml_helper.Medi_Checker):
    return {'Covid': ml_helper.predict(symptoms)}


@router.post('/api/medi_checker/from_xray')
async def predict_health_from_image(file: UploadFile = File(...)):
    result = await dl_helper.predict(file)
    return {dl_helper.class_list[i]: float(result[i]) for i in range(len(dl_helper.class_list)) if dl_helper.class_list[i] not in dl_helper.ext_class}


# Get Max Oxygen that can be Requested by User

@router.post('/api/oxygen/max')
async def get_max_oxygen(                  
                            age: int = 0,
                            gender: int = 3,
                            asthma: Union[bool, int] = 0,
                            pneumonia: Union[bool, int] = 0,
                            other_lung_disease: Union[bool, int] = 0,
                            breathing_difficulty: Union[bool, int] = 0,
                            fever: Union[bool, int] = 0,
                            cough: Union[bool, int] = 0,
                            sore_throat: Union[bool, int] = 0,
                            chest_pain: Union[bool, int] = 0,
                            contact_with_covid_patient: Union[bool, int] = 0,
                            travel_history: Union[bool, int] = 0,
                            attended_large_gathering: Union[bool, int] = 0,
    ):

    pred = ml_helper.predict(ml_helper.Medi_Checker(**{
        'breathing_problem': breathing_difficulty,
        'fever': fever,
        'dry_cough': cough,
        'sore_throat': sore_throat,
        'abroad_travel': travel_history,
        'contact_with_covid_patient': contact_with_covid_patient,
        'attended_large_gathering': attended_large_gathering
    }))

    if pred >= 0.75:
        max_limit = 9999;
    elif pred >= 0.55:
        max_limit = 99
    elif pred > 0.40:
        max_limit = 75
    else:
        max_limit = 50

    return {'max_limit': max_limit}


@router.post('/api/feedback')
async def feedback(value: models.FeedBack, db: Session = Depends(get_db)) -> models.FeedBack:
    return crud.upload_feedback(db, value)