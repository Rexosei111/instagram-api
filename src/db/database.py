from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker
from typing import AsyncGenerator
from settings import get_settings

settings = get_settings()

engine = create_async_engine(settings.sqlalchemy_database_url)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)

Base: DeclarativeMeta = declarative_base()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
