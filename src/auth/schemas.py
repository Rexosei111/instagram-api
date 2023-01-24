from typing import Optional, Generic
import datetime
import uuid
from pydantic import EmailStr
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate, CreateUpdateDictModel
from fastapi_users import models


class User(Generic[models.ID], CreateUpdateDictModel):
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
