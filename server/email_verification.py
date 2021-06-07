from typing import Literal, Union

from sqlalchemy.sql.expression import false
from .environ import Config
from jose import JWTError, jwt
from fastapi import status, HTTPException
from . import crud, schema

SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM

def generate_confirmation_token(email) -> str:
    '''Generate New Verification Token'''
    return jwt.encode({"sub": email}, SECRET_KEY, algorithm=ALGORITHM)

def confirm_token(token: str) -> Union[str, None]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
    except JWTError:
        raise None
