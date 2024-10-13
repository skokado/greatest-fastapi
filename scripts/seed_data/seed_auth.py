from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.tests.factories.user_factory import UserFactory
from app.auth.utils.password import hash_password


async def main(session: AsyncSession):
    # --- User
    print("# --- Seed User")
    await UserFactory.create(session, email="terutacchi@gmail.com", hashed_password=hash_password("password"))
    await UserFactory.create_batch(session, 10, commit=True)
