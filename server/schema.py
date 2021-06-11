# Objects representing actual Relations in the Database

from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Column, String, Date, Integer, BigInteger, Boolean, ForeignKey, Time, Numeric

class User(Base):
    __tablename__ = "user_login_detail_general"

    user_id = Column(String, primary_key=True)
    password = Column(String)
    is_active = Column(Boolean)
    is_confirmed = Column(Boolean)
    first_name = Column(String)
    last_name = Column(String)
    email_id = Column(String)
    dob = Column(Date)
    pin = Column(Integer)
    contact_no = Column(BigInteger)
    latitude = Column(Numeric)
    longitude = Column(Numeric)

class Admin(Base):
    __tablename__ = "admin_login_detail"

    user_id = Column(String, ForeignKey(User.user_id), primary_key=True)
    user_obj: User = relationship('User')
    workspace = Column(String)
    designation = Column(String)
    experience = Column(Integer)
    license_id = Column(Integer)


class Doctor(Base):
    __tablename__ = "doctor_db"

    user_id = Column(String, ForeignKey(User.user_id), primary_key=True)
    user_obj: User = relationship('User')
    specialization = Column(String)
    visiting_hr = Column(Time)
    fees = Column(Integer)
    assistant_contact_no = Column(BigInteger)
    website = Column(String)
    chamber_city = Column(String)


class Vendor(Base):
    __tablename__ = "vendor_db"

    user_id = Column(String, ForeignKey(User.user_id), primary_key=True)
    user_obj: User = relationship('User')
    store_name = Column(String)
    country = Column(String)
    state = Column(String)
    district = Column(String)
    city_or_village_name = Column(String)
    store_contact_no = Column(BigInteger)
    wp_no = Column(Integer)
    delivery_capacity = Column(BigInteger)
    store_id = Column(String)


class VendorProduct(Base):
    __tablename__ = "vendor_product_detail"
    
    product_id = Column(String, primary_key=True)
    store_id = Column(String, ForeignKey(Vendor.store_id))
    vendor_obj: Vendor = relationship('Vendor')
    store_name = Column(String)
    quantity = Column(Integer)
    price = Column(Integer)
    delivery_eta = Column(String)
    feedback = Column(String)
    is_oxygen = Column(Boolean)


class Ambulance(Base):
    __tablename__ = "ambulance_db"

    store_id = Column(String, primary_key=True)
    org_name = Column(String)
    contact_no = Column(Integer)
    car_no = Column(Integer)


class AppointmentListForUser(Base):
    __tablename__ = "appointment_list_for_user"

    doc_user_id = Column(String, ForeignKey(Doctor.user_id), primary_key=True)
    doc_obj: Doctor = relationship('Doctor')
    appoinment_day = Column(Date)
    time = Column(Time)
    fees = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    chamber_city = Column(String)
    doc_contact = Column(BigInteger)


class UserMedicine(Base):
    __tablename__ = "user_medicine_db"

    user_id = Column(String, primary_key=True)
    store_id = Column(String)
    product_id = Column(String, ForeignKey(VendorProduct.product_id))
    product_obj: VendorProduct = relationship('VendorProduct')
    date_of_purchase = Column(Date)
    bill_id = Column(String)


class UserOxygen(Base):
    __tablename__ = "user_oxygen_db"

    user_id = Column(String, primary_key=True)
    store_id = Column(String)
    product_id = Column(String, ForeignKey(VendorProduct.product_id))
    product_obj: VendorProduct = relationship('VendorProduct')
    price = Column(Integer)
    date_of_delivery = Column(Date)
    quantity = Column(Integer)