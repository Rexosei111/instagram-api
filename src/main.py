from fastapi import FastAPI, Depends
from auth.router import get_current_active_user, auth_router, register_router, verify_router, reset_password_router, users_router
import uvicorn
from db.database import create_db_and_tables
from auth.models import User

app = FastAPI()

app.include_router(auth_router, prefix="/auth/jwt", tags=["Auth"])
app.include_router(register_router, prefix="/auth", tags=["Auth"])
app.include_router(verify_router, prefix="/auth", tags=["Auth"])
app.include_router(reset_password_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(get_current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="info", reload=True)
