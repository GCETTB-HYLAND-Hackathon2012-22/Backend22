# Collections of all pydantic models

from datetime import date
from pydantic import BaseModel

class UserBase(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email_id: str
    dob: date
    pin: int
    contact_no: int

class UserCreate(UserBase):
    password: str

class User(UserBase):
    is_active: bool
    is_confirmed: bool
    
    class Config:
        orm_mode = True

class Admin(BaseModel):
    user_obj: User

    class Config:
        orm_mode = True

class Doctor(BaseModel):
    user_obj: User

    class Config:
        orm_mode = True

class Vendor(BaseModel):
    user_obj: User

    class Config:
        orm_mode = True