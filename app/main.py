from fastapi import FastAPI

from config import settings


app = FastAPI(
    title=settings.title,
    debug=settings.DEBUG,
    docs_url=settings.docs_url,
)


@app.get("/")
def ping():
    return {"message": "it works"}


# Register App routers
# ruff: noqa: E402
from auth.routers import router as auth_router

app.include_router(auth_router, prefix="/auth")
