from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from common.dependencies import get_db

app = FastAPI(
    title=settings.title,
    debug=settings.DEBUG,
    docs_url=settings.docs_url,
)


@app.get("/")
def hello():
    return {"message": "it works"}


@app.get("/ping")
async def pong(db: AsyncSession = Depends(get_db)):
    from auth.models import User

    stmt = select(User).where(User.email == "spongebob@example.com")
    user = (await db.execute(stmt)).scalar_one_or_none()
    return {"ping": "pong"}
