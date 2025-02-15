from http import HTTPStatus

import pytest

from app.common.database import get_session
from app.common.dependencies import is_valid
from app.v1.logic import create_user, get_all_users
from app.v1.schema import UserSchema

V1_ENDPOINT = "/v1"


@pytest.fixture
def dependency_overrides(application, get_test_session):
    application.dependency_overrides[is_valid] = lambda: None
    application.dependency_overrides[get_session] = get_test_session
    yield application.dependency_overrides
    application.dependency_overrides = {}


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_get_users(client, user_factory):
    user = await user_factory(name="testuser")

    response = await client.get(f"{V1_ENDPOINT}/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["users"]
    assert response.json()["users"][0]["id"] == user.id
    assert response.json()["users"][0]["name"] == user.name


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_get_user(client, test_session):
    user_schema = UserSchema(name="testuser")
    user = await create_user(test_session, user_schema)

    response = await client.get(f"{V1_ENDPOINT}/user/{user.uuid}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["user"]
    assert response.json()["user"]["id"] == user.id
    assert response.json()["user"]["name"] == user.name


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_create_user(client, test_session):
    payload = {"name": "testuser"}

    response = await client.post(f"{V1_ENDPOINT}/users", json=payload)

    users = await get_all_users(test_session)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["user"]
    assert len(users) == 1
