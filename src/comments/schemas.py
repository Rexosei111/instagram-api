from datetime import datetime

from auth.schemas import User
from sqlmodel import SQLModel

from .models import CommentBase


class CommentRead(SQLModel):
    id: int
    text: str
    created_at: datetime
    updated_at: datetime
    post_id: int
    user: User


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass
