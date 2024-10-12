from datetime import datetime, timezone
import pytest
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ...models import User


@pytest.mark.asyncio
async def test_foo(session: AsyncSession):
    spongebob = User(
        email="spongebob@example.com",
        hashed_password="hashed_password",
        is_active=True,
        first_name="Spongebob",
        last_name="Squarepants",
        updated_at=datetime.now(tz=timezone.utc),
    )
    session.add(spongebob)
    await session.flush()

    # stmt = select(func.count("*")).select_from(User)
    stmt = select(User).where(User.email == "spongebob@example.com")
    response = await session.execute(stmt)
    
    user = response.scalar_one_or_none()
    assert user.email == "spongebob@example.com"
