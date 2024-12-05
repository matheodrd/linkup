import os
from typing import Dict
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.database_setup import create_db_and_tables
from app.routes.users import router as user_router
from app.routes.posts import router as post_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Link Up", lifespan=lifespan)

if not os.getenv("ENVIRONMENT") == "production":
    app.mount("/static/medias", StaticFiles(directory="static/medias"), name="medias")

app.include_router(user_router)
app.include_router(post_router)

@app.get("/")
async def index() -> Dict[str, str]:
    return {"message": "hello amigo :-)"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
