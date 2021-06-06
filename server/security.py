# Handles Login

from starlette.responses import HTMLResponse
from server import models
from typing import Literal, Union
from . import crud, schema
from .environ import Config
from .database import get_db
from .router import router
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_DAYS = 3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth")


def get_password_hash(password: str) -> str:
    '''Encodes password by hashing technique'''
    return str(pwd_context.hash(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''Verify weather the given plain password and the hashed password are same or not'''
    return bool(pwd_context.verify(plain_password, hashed_password))


def authenticate_user(db: Session, uid: str, password: str) -> Union[schema.User, Literal[False]]:
    '''Authenticate User'''
    user = crud.get_user(db, uid)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict) -> str:
    '''Generate New Token'''
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> schema.User:
    '''Retrive Current User'''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: str = payload.get("sub")
        if uid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user(db, uid)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schema.User = Depends(get_current_user)) -> schema.User:
    '''Retrive Current User and also check if the user is active or not'''
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


##############################################################################################


@router.post('/api/auth')
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    '''Authentication Endpoint'''
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.user_id, "exp": datetime.utcnow() + access_token_expires}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/api/register', response_model=models.User)
async def register(user: models.UserCreate, db: Session = Depends(get_db)):
    # TODO: Check for duplicate values
    user.password = get_password_hash(user.password)
    return crud.create_user(db, user)


@router.get("/api/users/me", response_model=models.User)
async def read_users_me(current_user: schema.User = Depends(get_current_active_user)):
    return current_user


@router.get("/api/users/me_as_admin", response_model=models.Admin)
async def read_users_me(db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_active_user)):
    admin = crud.get_admin(db, current_user.user_id)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin Permission Not Found",
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return admin;