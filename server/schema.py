# Objects representing actual Relations in the Database

from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Column, String, Date, Integer, BigInteger, Boolean, ForeignKey, Time

class User(Base):
    __tablename__ = "user_login_detail_general"

    user_id = Column(String, primary_key=True)
    password = Column(String)
    is_active = Column(Boolean)
    first_name = Column(String)
    last_name = Column(String)
    email_id = Column(String)
    dob = Column(Date)
    pin = Column(Integer)
    contact_no = Column(BigInteger)

class Admin(Base):
    __tablename__ = "admin_login_detail"

    user_id = Column(String, ForeignKey(User.user_id), primary_key=True)
    user_obj = relationship('User')
    workspace = Column(String)
    designation = Column(String)
    experience = Column(Integer)
    license_id = Column(Integer)


class Doctor(Base):
    __tablename__ = "doctor_db"

    user_id = Column(String, ForeignKey(User.user_id), primary_key=True)
    user_obj = relationship('User')
    specialization = Column(String)
    visiting_hr = Column(Time)
    fees = Column(Integer)
    assistant_contact_no = Column(Integer)
    website = Column(String)


class Vendor(Base):
    __tablename__ = "vendor_db"

    user_id = Column(String, ForeignKey(User.user_id), primary_key=True)
    user_obj = relationship('User')
    country = Column(String)
    state = Column(String)
    district = Column(String)
    city_or_village_name = Column(String)
    store_contact_no = Column(Integer)
    wp_no = Column(Integer)
    delivery_capacity = Column(Integer)
    store_id = Column(String)
    vendor_products = relationship('Vendor_Product')


class Vendor_Product(Base):
    __tablename__ = "vendor_product_detail"
    
    product_id = Column(String, primary_key=True)
    store_id = Column(String, ForeignKey('Vendor'))
    store_name = Column(String)
    quantity = Column(Integer)
    price = Column(Integer)
    delivery_eta = Column(String)
    feedback = Column(String)