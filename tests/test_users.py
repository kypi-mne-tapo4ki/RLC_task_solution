import pytest
from fastapi import status
from httpx import AsyncClient


pytestmark = pytest.mark.anyio


async def test_user_registration(client: AsyncClient) -> None:
    username = "test_user_1"
    response = await client.post(
        "/users/registration",
        params={"username": username},
    )
    assert response.status_code == status.HTTP_200_OK

    user_dict = response.json()
    assert "token" in user_dict

    response = await client.post(
        "/users/registration",
        params={"username": username},
    )
    assert response.status_code == status.HTTP_200_OK

    updated_user_dict = response.json()
    assert "token" in updated_user_dict
    assert user_dict["token"] != updated_user_dict["token"]


async def test_check_user(client: AsyncClient) -> None:
    username = "test_user_2"
    response = await client.post(
        "/users/registration",
        params={"username": username},
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["token"]

    response = await client.get(
        "/users/user_check",
        params={"token": token},
    )
    user_dict = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert user_dict["username"] == username
