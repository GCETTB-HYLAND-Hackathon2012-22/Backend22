# Collections of all pydantic models

from datetime import date, time
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
    latitude: float = None
    longitude: float = None

class User(UserBase):
    is_active: bool
    is_confirmed: bool
    
    class Config:
        orm_mode = True

class Admin(BaseModel):
    user_obj: User
    workspace: str
    designation: str
    experience: int
    license_id: int

    class Config:
        orm_mode = True

class Doctor(BaseModel):
    user_obj: User
    specialization: str
    visiting_hr: time
    fees: int
    assistant_contact_no: int
    website: str
    chamber_city: str

    class Config:
        orm_mode = True

class Vendor(BaseModel):
    user_obj: User
    store_name: str
    country: str
    state: str
    district: str
    city_or_village_name: str
    store_contact_no: int
    wp_no: int
    delivery_capacity: int

    class Config:
        orm_mode = True

class VendorProduct(BaseModel):
    product_id: str
    store_id: str
    vendor_obj: Vendor
    store_name: str
    quantity: int
    price: int
    delivery_eta: date
    feedback: str

    class Config:
        orm_mode = True

class AppointmentListForUser(BaseModel):
    doc_user_id: str
    appoinment_day: date
    time: time
    fees: int
    first_name: str
    last_name: str
    chamber_city: str
    doc_contact: int
    problem: str

    class Config:
        orm_mode = True


class UserMedicineBase(BaseModel):
    user_id: str
    store_id: str
    product_id: str
    date_of_purchase: date
    bill_id: str

class UserMedicine(UserMedicineBase):
    product_obj: VendorProduct

    class Config:
        orm_mode = True


class UserOxygenBase(BaseModel):
    user_id: str
    store_id: str
    product_id: str
    price: int
    date_of_delivery: date
    quantity: int
    address: str

class UserOxygen(UserOxygenBase):
    product_obj: VendorProduct

    class Config:
        orm_mode = True
