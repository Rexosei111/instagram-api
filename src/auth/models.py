import uuid
from datetime import date
from typing import List
from typing import Optional
from typing import Union

from fastapi import Depends
from fastapi import Request
from fastapi_users import BaseUserManager
from fastapi_users import InvalidPasswordException
from fastapi_users import UUIDIDMixin
from fastapi_users_db_sqlalchemy.generics import GUID
from settings import get_settings
from sqlalchemy import Column
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

from .dependencies import get_user_db
from .schemas import UserCreate


settings = get_settings()


class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(
        sa_column=(Column(GUID, primary_key=True, default=uuid.uuid4))
    )
    email: str = Field(max_length=320, unique=True, index=True, nullable=False)
    hashed_password: str = Field(max_length=1024, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)
    is_verified: bool = Field(default=False, nullable=False)
    fullname: str = Field()
    birthdate: Optional[date] = Field(nullable=True)
    posts: List["Post"] = Relationship(back_populates="user")


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.reset_password_token_secret
    verification_token_secret = settings.verification_token_secret

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(reason="Password should not contain e-mail")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
