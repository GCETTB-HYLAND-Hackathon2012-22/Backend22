# CREATE, READ, UPDATE, DELETE

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