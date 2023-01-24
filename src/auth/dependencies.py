from fastapi import Depends
from db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    # Trying to avoid circular import
    from .models import User

    yield SQLAlchemyUserDatabase(session, User)
