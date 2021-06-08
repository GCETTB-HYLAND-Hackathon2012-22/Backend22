import pathlib
from typing import Union
from fastapi import HTTPException, status, Depends
from fastapi.responses import HTMLResponse

from .environ import Config
from .router import router
from . import crud, schema
from .database import get_db, Session
from jose import JWTError, jwt

import smtplib, ssl


SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM

def generate_confirmation_token(email: str) -> str:
    '''Generate New Verification Token'''
    return jwt.encode({"sub": email}, SECRET_KEY, algorithm=ALGORITHM)

def confirm_token(token: str) -> Union[str, None]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
    except JWTError:
        raise None


##########################################################

port = 465  # For SSL
password = str(Config.MAIL_PASSWORD)
sender_email = str(Config.MAIL_ID)

message = """\
Subject: Confirmation Mail for Signing-Up in Health is Wealth

This email account has been registered into our website.
Is it you?!! or any other else.

Confirm Your Signing-Up by activating your account.

To activate your account please follow this link:
http://gcettbiaans22.herokuapp.com%s
"""

# Create a secure SSL context
context = ssl.create_default_context()

def send_confirmation_mail(email: str) -> None: 
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        token: str = generate_confirmation_token(email)

        m = message %router.url_path_for('confirm_token_endpoint', **{"token": token})

        # Send email here
        server.sendmail(sender_email, email, m)


@router.get('/api/users/confirm/{token}', response_class=HTMLResponse)
async def confirm_token_endpoint(token: str, db: Session = Depends(get_db)):
    error = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Url"
        )
    email = confirm_token(token)
    if not email:
        raise error
    
    user: schema.User = crud.get_user_email(db, email)
    if not user:
        raise error
    
    user.is_confirmed = True
    crud.update_user(db, user)
    return pathlib.Path(__file__).parent.parent/'pages'/'email_confirmed.html'