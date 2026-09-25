"""Database engine and session management (Database Integration task).

Only the plumbing exists today: an async SQLAlchemy engine/session factory
created lazily on first use. No endpoint touches the database yet, and the
application starts fine without PostgreSQL — that wiring is the Database
Integration task.

TODO(Database Integration task):
  * define ORM models in `app/models/` (inheriting `app.database.base.Base`)
  * add Alembic migrations
  * use `get_db_session` in services/repositories
  * verify connectivity during application startup
"""
from __future__ import annotations

import logging
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings, get_settings
from app.core.exceptions import DatabaseNotConfiguredError

logger = logging.getLogger(__name__)

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine(settings: Settings | None = None) -> AsyncEngine:
    """Return the process-wide async engine, creating it on first use.

    Raises:
        DatabaseNotConfiguredError: when `DATABASE_URL` is not set.
    """
    global _engine

    if _engine is None:
        settings = settings or get_settings()
        if not settings.database_url:
            raise DatabaseNotConfiguredError(
                "DATABASE_URL is not set. Add it to .env before using "
                "database-backed features (Database Integration task)."
            )
        _engine = create_async_engine(
            settings.database_url,
            echo=settings.db_echo,
            pool_pre_ping=True,
        )
        logger.info("SQLAlchemy async engine created.")

    return _engine


def get_session_factory(settings: Settings | None = None) -> async_sessionmaker[AsyncSession]:
    """Return the session factory bound to the lazily created engine."""
    global _session_factory

    if _session_factory is None:
        _session_factory = async_sessionmaker(
            bind=get_engine(settings),
            expire_on_commit=False,
            autoflush=False,
        )

    return _session_factory


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency yielding one session per request.

    Not used by any endpoint yet. When database access is needed:

        from typing import Annotated
        from fastapi import Depends
        from sqlalchemy.ext.asyncio import AsyncSession

        DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def dispose_engine() -> None:
    """Dispose of the engine and reset module state (called on app shutdown)."""
    global _engine, _session_factory

    if _engine is not None:
        await _engine.dispose()
        logger.info("SQLAlchemy async engine disposed.")

    _engine = None
    _session_factory = None