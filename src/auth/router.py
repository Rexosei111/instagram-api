from .utils import fastapi_users, auth_backend
from .schemas import UserCreate, User, UserUpdate


auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router(User, UserCreate)
verify_router = fastapi_users.get_verify_router(User)
reset_password_router = fastapi_users.get_reset_password_router()
users_router = fastapi_users.get_users_router(User, UserUpdate)

get_current_active_user = fastapi_users.current_user(active=True)
