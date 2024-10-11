from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config.db import engine

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
