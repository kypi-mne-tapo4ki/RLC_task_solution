import pytest
from fastapi import status
from httpx import AsyncClient


pytestmark = pytest.mark.anyio


async def test_create_record(client: AsyncClient) -> None:
    response = await client.post(
        "/users/registration",
        params={"username": "new_user"},
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["token"]
    payload = {
        "title": "Test Record",
        "content": "This is a test record content.",
        "tag": "test_tag",
        "token": token,
    }
    response = await client.post(
        "/records",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    response_dict = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_dict["title"] == payload["title"]
    assert response_dict["content"] == payload["content"]
    assert response_dict["tag"] == payload["tag"]


async def test_read_records(client: AsyncClient) -> None:
    response = await client.get("/records")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


async def test_read_record(client: AsyncClient) -> None:
    record_id = 1
    response = await client.get(f"/records/{record_id}")
    assert response.status_code == status.HTTP_200_OK
    assert "title" in response.json()


async def test_update_record(client: AsyncClient) -> None:
    response = await client.post(
        "/users/registration",
        params={"username": "any_user"},
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["token"]

    record_id = 1
    payload = {
        "title": "Updated Record Title",
    }
    response = await client.patch(
        f"/records/{record_id}",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    response_dict = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert "title" in response_dict
    assert response_dict["title"] == payload["title"]


async def test_delete_record(client: AsyncClient) -> None:
    response_token = await client.post(
        "/users/registration",
        params={"username": "any_user"},
    )
    assert response_token.status_code == status.HTTP_200_OK
    token = response_token.json()["token"]

    record_id = 1
    response = await client.delete(
        f"/records/{record_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
