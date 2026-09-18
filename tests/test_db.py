"""Engine and session factory wiring; no live database needed"""

from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Base, engine, session_factory


def test_engine_talks_to_postgres_over_asyncpg() -> None:
    assert engine.url.get_backend_name() == "postgresql"
    assert engine.url.get_driver_name() == "asyncpg"


def test_engine_pool_is_configured() -> None:
    assert engine.pool.size() == 5
    assert engine.pool._pre_ping is True


def test_naming_convention_is_set() -> None:
    assert set(Base.metadata.naming_convention) == {"ix", "uq", "ck", "fk", "pk"}


async def test_session_factory_returns_async_session() -> None:
    async with session_factory() as session:
        assert isinstance(session, AsyncSession)
        assert session.sync_session.expire_on_commit is False
