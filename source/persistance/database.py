from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import contextlib
from typing import AsyncIterator, Any

from sqlalchemy import insert
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection

import logging
from .models import ViewKind, ViewKindVariant, BaseModel


_logger = logging.getLogger(__name__)
__all__ = ["DatabaseContext"]


class DatabaseContext:
    """
    Manages database sessions and connections for an application.

    :ivar _engine: The SQLAlchemy async engine.
    :vartype _engine: AsyncEngine
    :ivar _sessionmaker: A factory for creating new AsyncSession instances.
    :vartype _sessionmaker: sessionmaker
    """

    def __init__(self, uri: str, **kwargs: Any):
        """
        Initializes the instance.

        :param uri: Database URI.
        :type uri: str

        :param kwargs: Additional arguments to pass to the engine creator, defaults to None.
        :type kwargs: dict[str, any] | None, optional
        """

        # Guards kwargs.
        kwargs.setdefault("future", True)

        # Initializes attributes.
        self._engine = create_async_engine(url=uri, **kwargs)
        self._sessionmaker = async_sessionmaker(bind=self._engine, autoflush=True, expire_on_commit=True, autocommit=False, future=True)
        _logger.info("Database context has been initialized")

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncSession]:
        """
        Provides an asynchronous context manager for raw database connections.

        :yields: A raw database connection.
        :rtype: AsyncConnection

        :raises Exception: If the engine is not initialized.
        """

        # Guards initialization.
        if self._engine is None:
            raise Exception("Database context is not initialized")

        # Manages connection.
        async with self._engine.begin() as connection:
            connection: AsyncConnection

            try:
                yield connection

            except Exception:
                _logger.error("An error occurred during database connection")
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Provides an asynchronous context manager for managing database sessions.

        :yields: A session for interacting with the database.
        :rtype: AsyncSession

        :raises Exception: If the sessionmaker is not initialized.
        """

        # Guards initialization.
        if self._sessionmaker is None:
            raise Exception("Database context is not initialized")

        # Manages session.
        async with self._sessionmaker() as session:
            session: AsyncSession

            try: yield session

            except Exception:
                _logger.error("An error occurred during database session")
                await session.rollback()
                raise


    async def close(self):
        """
        Disposes the engine, closing all active connections.
        """

        # Disposes disposables.
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

        _logger.info("Database context has been closed")
