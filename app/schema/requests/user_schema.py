from typing import Optional

from fastapi import Depends, Request, Form, Path
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr

from app.services.password_service import PasswordService


class CurrentUserRequest:
    def __init__(self,
                 req: Request,
                 test : str = Path(...),
                 token: Optional[str] = Depends(OAuth2PasswordBearer(tokenUrl="token"))
                 ):
        self.token = token


class CreateUserRequest:
    def __init__(self,
                 req: Request,
                 username: str = Form(...),
                 password: str = Form(...),
                 email: EmailStr = Form(...),
                 phone_number: str = Form(...),
                 name: str = Form(...)
                 ):
        self.username = username
        self.password = PasswordService.get_hashed_password(password)
        self.email = email
        self.name = name
        self.phone_number = phone_number


class ResetPasswordRequest:
    def __init__(self,
                 req : Request,
                 username:str = Form(...),
                 email:EmailStr = Form(...)
                 ):
        self.username = username
        self.email = email
