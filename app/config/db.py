from typing import TYPE_CHECKING
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings

if TYPE_CHECKING:
    from sqlalchemy.orm.decl_api import DeclarativeMeta


Base: "DeclarativeMeta" = declarative_base()
engine = create_async_engine(settings.DATABASE_URL, echo=True)
