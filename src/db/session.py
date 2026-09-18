"""Async engine and session factory"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

engine = create_async_engine(
    settings.database_url.get_secret_value(),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=5,
)

session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def ping() -> None:
    """Run SELECT 1, raising if the database is unreachable"""
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))


async def dispose() -> None:
    """Close every pooled connection"""
    await engine.dispose()
