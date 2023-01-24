from pydantic import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    jwt_secret: str
    jwt_expire_time: Optional[int] = 3000
    sqlalchemy_database_url: str
    reset_password_token_secret: str
    verification_token_secret: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
