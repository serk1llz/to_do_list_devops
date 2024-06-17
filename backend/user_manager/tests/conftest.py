import asyncio
from typing import AsyncGenerator
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import settings
from main import app
from db.models import metadata_obj
from db.database import get_async_session
from httpx import AsyncClient
from sqlalchemy.sql import text

engine_test = create_async_engine(settings.database_url_test, echo=False)
async_session_maker = async_sessionmaker(
    bind=engine_test,
    autocommit=False,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
)
metadata_obj.bind = engine_test


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


@pytest.fixture(scope="session", autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
