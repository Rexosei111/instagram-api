import datetime
from typing import Optional

from fastapi_users import models
from fastapi_users.schemas import (
    CreateUpdateDictModel,
)
from pydantic import EmailStr
from sqlmodel import SQLModel


class User(SQLModel):
    id: models.ID
    email: EmailStr
    fullname: str

    class Config:
        orm_mode = True


class UserCreate(CreateUpdateDictModel):
    email: EmailStr
    password: str
    fullname: str
    birthdate: Optional[datetime.date]


class UserUpdate(CreateUpdateDictModel):
    password: Optional[str]
    email: Optional[EmailStr]
    fullname: Optional[str]
    birthdate: Optional[datetime.date]
