from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs

from config import settings


class Base(AsyncAttrs, DeclarativeBase):
    pass


# async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)
