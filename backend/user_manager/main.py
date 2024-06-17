from fastapi_users import FastAPIUsers
from db.models import User
from user_manager import get_user_manager
from fastapi import FastAPI, Depends
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from schemas import UserRead, UserCreate
from auth import auth_backend

app = FastAPI()
origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Methods"],
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

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
