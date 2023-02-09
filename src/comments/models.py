from datetime import datetime
from typing import Optional
from uuid import UUID

from auth.models import User
from posts.models import Post
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel


class CommentBase(SQLModel):
    text: str


class Comment(CommentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=datetime.now())
    post_id: int = Field(foreign_key="post.id")
    post: Post = Relationship(back_populates="comments")
    user_id: UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="comments")
