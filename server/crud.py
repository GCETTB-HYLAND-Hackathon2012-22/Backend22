# CREATE, READ, UPDATE, DELETE

from typing import List
from sqlalchemy.orm import Session
from . import schema, models

def get_user(db: Session, uid: str) -> schema.User:
    return db.query(schema.User).filter(schema.User.user_id == uid).first()

def create_user(db: Session, user: models.UserCreate) -> schema.User:
    db_user = schema.User(**user.dict(), is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_admin(db: Session, uid: str) -> schema.Admin:
    return db.query(schema.Admin).filter(schema.Admin.user_id == uid).first()


def get_doctor(db: Session, uid: str) -> schema.Doctor:
    return db.query(schema.Doctor).filter(schema.Doctor.user_id == uid).first()

def get_doctors(db: Session, skip=0, limit=100) -> List[schema.Doctor]:
    return db.query(schema.Doctor).offset(skip).limit(limit).all()


def get_vendor(db: Session, uid: str) -> schema.Vendor:
    return db.query(schema.Vendor).filter(schema.Vendor.user_id == uid).first()

def get_vendors(db: Session, skip=0, limit=100) -> List[schema.Vendor]:
    return db.query(schema.Vendor).offset(skip).limit(limit).all()

