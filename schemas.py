from enum import Enum

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic.v1 import validator


class RoleEnum(str, Enum):
    #admin = "admin"
    client = "client"
    controller = "controller"


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    patronymic: str = None
    email: str
    role: RoleEnum
    photo: str = None

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    email: str
    role: RoleEnum


class RegistrationConfirm(LoginUser):
    code: int


class AuthCheck(RegistrationConfirm):
    pass