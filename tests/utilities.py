from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import TESTING_CONFIG

ENGINE = create_async_engine(
    TESTING_CONFIG.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)


async def get_test_session():
    async with SessionLocal() as session:
        yield session
