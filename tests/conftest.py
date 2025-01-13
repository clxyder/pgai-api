import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app import create_app
from app.common import models
from tests.utilities import ENGINE, SessionLocal


@pytest.fixture(name="application")
def fixture_application():
    """Fixture to set up application with configuration

    Returns:
        application -- Application context
    """
    app = create_app()

    asyncio.run(create_tables())

    yield app


async def create_tables():
    async with ENGINE.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


@pytest.fixture(name="client")
def fixture_client(application):
    """Fixture for HTTP test client

    Arguments:
        application -- Application context

    Returns:
        client -- HTTP client
    """
    return TestClient(application)


@pytest_asyncio.fixture(name="test_session")
async def fixture_test_session():
    async with SessionLocal() as session:
        yield session
