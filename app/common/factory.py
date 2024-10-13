from typing import Generic, Type, TypeVar
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from config.db import Base as ModelBase

T = TypeVar("T", bound=ModelBase)


class BaseFactory(SQLAlchemyModelFactory, Generic[T]):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "flush"

        # FIXME: Type variable "app.auth.tests.factories.user_factory.T" is unbound
        # but this works.
        model: Type[T]

    @classmethod
    async def create(cls, session: AsyncSession, commit: bool = False, **overrides) -> T:
        obj: T = cls.build(**overrides)
        session.add(obj)
        if commit:
            await session.commit()
        else:
            await session.flush()
        return obj

    @classmethod
    async def create_batch(
        cls, session: AsyncSession, size: int, commit: bool = False, **overrides
    ) -> list[User]:
        return [await cls.create(session, commit, **overrides) for _ in range(size)]
