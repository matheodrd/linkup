from typing import Dict
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from database_setup import create_db_and_tables
from routes.users import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Link Up", lifespan=lifespan)

app.include_router(user_router)

@app.get("/")
async def index() -> Dict[str, str]:
    return {"message": "hello amigo :-)"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
