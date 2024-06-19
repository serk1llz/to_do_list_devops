import pytest
from httpx import AsyncClient


async def test_register(ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "email": "test220@mail.ru",
            "password": "test",
        },
    )

    assert response.status_code == 201


async def test_login(ac: AsyncClient):
    response = await ac.post(
        "/auth/jwt/login",
        data={
            "username": "test220@mail.ru",
            "password": "test",
        },
    )

    assert response.status_code == 204


async def test_not_valid_data_register(ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "email": "test10",
            "password": "test",
        },
    )

    assert response.status_code == 422


async def test_not_valid_data_login(ac: AsyncClient):
    response = await ac.post(
        "/auth/jwt/login",
        data={
            "username": "test10",
            "password": "test",
        },
    )

    assert response.status_code == 400
