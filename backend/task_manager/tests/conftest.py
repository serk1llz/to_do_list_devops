import asyncio
from typing import AsyncGenerator

import pytest
from config import settings
from main import app
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql import text
from src.db.database import get_async_session
from src.db.models import User, metadata_obj
from src.services.services import TaskService

engine_test = create_async_engine(settings.database_url_test, echo=False)
async_session_maker = async_sessionmaker(
    bind=engine_test,
    autocommit=False,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
)
metadata_obj.bind = engine_test
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS to_do_list;"))
        await conn.run_sync(metadata_obj.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)
        await conn.execute(text(f"DROP SCHEMA IF EXISTS to_do_list CASCADE;"))


@pytest.fixture(scope="session")
async def create_user():
    async def _create_user(email: str, password: str):
        hashed_password = pwd_context.hash(password)
        async with async_session_maker() as session:
            async with session.begin():
                user = User(email=email, hashed_password=hashed_password, role="User")
                session.add(user)
                await session.flush()
                user_id = user.id
                await session.commit()
                return user_id

    return _create_user


@pytest.fixture(scope="session", autouse=True)
async def task_service(create_user):
    user_id = await create_user(email="test@mail.ru", password="test")
    async with async_session_maker() as session:
        task_service = TaskService(user_id, session)
        yield task_service


@pytest.fixture(scope="session", autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
