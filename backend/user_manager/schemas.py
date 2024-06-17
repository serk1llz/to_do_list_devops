from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(             schemas.BaseUser[int]):
    email: EmailStr


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
