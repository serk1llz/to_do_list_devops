import uvicorn
from auth import auth_backend
from db.models import User
from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers
from schemas import UserCreate, UserRead
from starlette.middleware.cors import CORSMiddleware
from user_manager import get_user_manager

app = FastAPI()
origins = [
    "http://185.27.192.116:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Methods",
    ],
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
