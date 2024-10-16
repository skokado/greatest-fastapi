from httpx import AsyncClient
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User

from ..factories.user_factory import UserFactory


@pytest.mark.asyncio
async def test_foo(client: AsyncClient, session: AsyncSession):
    spongebob = await UserFactory.create(session, email="spongebob@example.com")

    stmt = select(User).where(User.email == "spongebob@example.com")
    user = (await session.execute(stmt)).scalar_one_or_none()
    assert user
    assert user.email == "spongebob@example.com"

    response = await client.get("/")
    assert response.status_code == 200
