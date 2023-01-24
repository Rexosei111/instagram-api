from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from settings import get_settings
from .models import get_user_manager, User
import uuid
from fastapi_users import FastAPIUsers

settings = get_settings()


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.jwt_secret, lifetime_seconds=settings.jwt_expire_time)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
