# Objects representing actual Relations in the Database

from .database import Base
from sqlalchemy import Column, String, Date, Integer, BigInteger, Boolean

class User(Base):
    __tablename__ = "user_login_detail_general"

    user_id = Column(String, unique=True, primary_key=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    first_name = Column(String)
    last_name = Column(String)
    email_id = Column(String, unique=True)
    dob = Column(Date)
    pin = Column(Integer)
    contact_no = Column(BigInteger, unique=True)