import os
from typing import AsyncGenerator, Generator

import asyncpg
import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

# ruff: noqa: E402
os.environ["DATABASE_NAME"] = "test_db"

from config.db import Base
from config import settings
from common.dependencies.db import get_db
from main import app


async def asyncpg_create_database_if_not_exists(url: str):
    """Create database test_db if not exists"""
    dsn = url.replace("+asyncpg", "")
    try:
        conn: asyncpg.Connection = await asyncpg.connect(dsn=dsn)
    except:  # noqa: E722
        conn: asyncpg.Connection = await asyncpg.connect(
            dsn=dsn.replace(f"/{settings.DATABASE_NAME}", "/postgres")
        )
        await conn.execute(f"CREATE DATABASE {settings.DATABASE_NAME}")

        # Check to newly created database
        conn = await asyncpg.connect(dsn=dsn)


@pytest.fixture()
async def session() -> AsyncGenerator[AsyncSession, None]:
    """Ref https://www.rhoboro.com/2021/06/12/async-fastapi-sqlalchemy.html"""

    # https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    async_engine = create_async_engine(settings.DATABASE_URL, echo=False)

    await asyncpg_create_database_if_not_exists(settings.DATABASE_URL)

    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()

        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        AsyncSessionLocal = async_sessionmaker(
            autoflush=False,
            bind=conn,
            future=True,
            class_=AsyncSession,
        )
        async_session = AsyncSessionLocal()

        def test_get_session() -> Generator:
            try:
                yield async_session
            except SQLAlchemyError:
                pass

        app.dependency_overrides[get_db] = test_get_session

        yield async_session

        await async_session.close()
        await conn.rollback()
        await conn.rollback()

    await async_engine.dispose()
