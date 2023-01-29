from datetime import datetime
from typing import Optional
from uuid import UUID

from auth import models
from pydantic import HttpUrl
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel


class PostBase(SQLModel):
    image_url: HttpUrl
    caption: Optional[str] = Field(default=None)


class Post(PostBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    timestamp: Optional[datetime] = Field(default=datetime.now())
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    user: Optional[models.User] = Relationship(back_populates="posts")
