# CREATE, READ, UPDATE, DELETE

from typing import List
from sqlalchemy.orm import Session
from . import schema, models


def get_user(db: Session, uid: str) -> schema.User:
    '''Returns User Details identified by uid'''
    return db.query(schema.User).filter(schema.User.user_id == uid).first()

def get_user_email(db: Session, email: str) -> schema.User:
    '''Returns User Details identified by email'''
    return db.query(schema.User).filter(schema.User.email_id == email).first()

def get_user_contact(db: Session, contact: int) -> schema.User:
    '''Returns User Details identified by contact'''
    return db.query(schema.User).filter(schema.User.contact_no == contact).first()

def update_user(db: Session, user: schema.User):
    db.add(user)
    db.commit()
    db.refresh(user)

def create_user(db: Session, user: models.UserCreate) -> schema.User:
    db_user = schema.User(**user.dict(), is_active=True, is_confirmed=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def verify_user(db: Session, user:)


def get_admin(db: Session, uid: str) -> schema.Admin:
    '''Returns Admin-User Details identified by uid'''
    return db.query(schema.Admin).filter(schema.Admin.user_id == uid).first()


def get_doctor(db: Session, uid: str) -> schema.Doctor:
    '''Returns Doctors Details identified by uid'''
    return db.query(schema.Doctor).filter(schema.Doctor.user_id == uid).first()

def get_doctors(db: Session) -> List[schema.Doctor]:
    '''Returns the list of all Doctors'''
    return db.query(schema.Doctor).all()


def get_vendor(db: Session, uid: str) -> schema.Vendor:
    '''Returns Vendors Details identified by uid'''
    return db.query(schema.Vendor).filter(schema.Vendor.user_id == uid).first()

def get_vendors(db: Session) -> List[schema.Vendor]:
    '''Returns the list of all Vendors'''
    return db.query(schema.Vendor).all()

def get_oxygen(db: Session) -> List[schema.VendorProduct]:
    '''Returns the list of all Oxygen as Products'''
    return db.query(schema.VendorProduct).filter(schema.VendorProduct.is_oxygen == True).all()

def get_medicine(db: Session) -> List[schema.VendorProduct]:
    '''Returns the list of all Oxygen as Products'''
    return db.query(schema.VendorProduct).filter(schema.VendorProduct.is_medicine == True).all()


def set_appointment(db: Session, appointment: models.AppointmentListForUser) -> schema.AppointmentListForUser:
    '''Fixes Appointment as set by user'''
    appointment = schema.AppointmentListForUser(**appointment.dict())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

def book_oxygen(item: models.UserOxygenBase, db: Session) -> schema.UserOxygen:
    '''Adds Order for Oxygen'''
    item = schema.UserOxygen(**item.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def book_medicine(item: models.UserMedicineBase, db: Session) -> schema.UserMedicine:
    '''Adds Order for Oxygen'''
    item = schema.UserMedicine(**item.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item