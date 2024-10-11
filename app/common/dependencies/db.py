from typing import AsyncGenerator, Generator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from config.db import engine, sync_engine

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
SessionLocal = sessionmaker(sync_engine, expire_on_commit=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()


def get_session() -> Generator[Session, None, None]:
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
