from fastapi import FastAPI

from config import settings

app = FastAPI(
    title=settings.title,
    debug=settings.DEBUG,
    docs_url=settings.docs_url,
)


@app.get("/")
def hello():
    return {"message": "it works"}
