import asyncio
from pathlib import Path
import sys

from factory.random import reseed_random

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, root_dir.as_posix())
sys.path.insert(1, (root_dir / "app").as_posix())

reseed_random(0)

# ruff: noqa: E402
from app.common.dependencies.db import AsyncSessionLocal


async def main():
    session = AsyncSessionLocal()
    try:
        from scripts.seed_data.seed_auth import main as seed_auth
        await seed_auth(session)
    except Exception as e:
        print(e)
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
