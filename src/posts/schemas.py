from datetime import datetime
from typing import Optional

from auth.schemas import User
from pydantic import HttpUrl
from sqlmodel import Field
from sqlmodel import SQLModel

from .models import PostBase


class PostRead(PostBase):
    id: int
    timestamp: datetime
    user: User


class PostCreate(PostBase):
    pass


class PostUpdate(SQLModel):
    image_url: Optional[HttpUrl] = Field(default=None)
    caption: Optional[str] = Field(default=None)
