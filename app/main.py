from fastapi import FastAPI

from config import settings

api = FastAPI(
    title=settings.title,
    debug=settings.DEBUG,
    docs_url=settings.docs_url,
)


@api.get("/")
def hello():
    return {"message": "it works"}
