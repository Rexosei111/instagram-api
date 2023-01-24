from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from db.database import Base
import uuid
from typing import Optional, Union
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, InvalidPasswordException
from .dependencies import get_user_db
from settings import get_settings
from .schemas import UserCreate
from datetime import date
from sqlalchemy import Column, String, Date


settings = get_settings()


class User(SQLAlchemyBaseUserTableUUID, Base):
    fullname: str = Column(String(50), nullable=False)
    birthdate: Optional[date] = Column(Date, nullable=True)


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
        print(
            f"Verification requested for user {user.id}. Verification token: {token}")

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
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
