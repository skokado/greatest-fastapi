import asyncio
from app.auth.tests.factories.user_factory import UserFactory

from app.common.dependencies.db import AsyncSessionLocal

async def main():
    session = AsyncSessionLocal()
    try:
        # --- User
        print("# --- Seed User")
        await UserFactory.create_batch(session, 10, commit=True)
    finally:
        await session.close()


asyncio.run(main())
