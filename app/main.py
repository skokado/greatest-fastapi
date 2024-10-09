from fastapi import FastAPI

from config import settings

api = FastAPI(settings=settings)


@api.get("/")
def hello():
    return {"message": "it works"}
