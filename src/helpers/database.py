from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

from .config import get_settings

SETTINGS = get_settings()
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{SETTINGS.POSTGRE_USERNAME}:{SETTINGS.POSTGRE_PASSWORD}@localhost/lms"

ENGINE = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={},
    future=True,
    echo=True,
)

AsyncSessionLocal = sessionmaker(
    bind=ENGINE,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)

BASE = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
