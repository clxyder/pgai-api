from http import HTTPStatus

import pytest

from app.common.database import get_session
from app.common.dependencies import is_valid
from app.v1.logic import create_page_content, get_all_pages
from app.v1.schema import PageSchema

V1_ENDPOINT = "/v1"


@pytest.fixture
def dependency_overrides(application, get_test_session):
    application.dependency_overrides[is_valid] = lambda: None
    application.dependency_overrides[get_session] = get_test_session
    yield application.dependency_overrides
    application.dependency_overrides = {}


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_get_pages(client, page_factory):
    page = await page_factory(title="testpage")

    response = await client.get(f"{V1_ENDPOINT}/pages")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["pages"]
    assert response.json()["pages"][0]["id"] == page.id
    assert response.json()["pages"][0]["title"] == page.title


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_get_page(client, test_session):
    page_schema = PageSchema(title="testpage", content="test content")
    page = await create_page_content(test_session, page_schema)

    response = await client.get(f"{V1_ENDPOINT}/pages/{page.uuid}")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["page"]
    assert response.json()["page"]["id"] == page.id
    assert response.json()["page"]["title"] == page.title


@pytest.mark.usefixtures("dependency_overrides")
@pytest.mark.asyncio
async def test_create_page_content(client, test_session):
    payload = {"title": "testpage", "content": "test content"}

    response = await client.post(f"{V1_ENDPOINT}/pages", json=payload)

    pages = await get_all_pages(test_session)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["page"]
    assert len(pages) == 1
