from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config import CONFIG

ENGINE = create_async_engine(CONFIG.DATABASE_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

Base = declarative_base()


async def get_session():
    async with SessionLocal() as session:
        yield session
