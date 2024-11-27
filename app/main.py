from typing import Dict

from fastapi import FastAPI
import uvicorn

from database_setup import create_db_and_tables

app = FastAPI(title="Link Up")

@app.get("/")
async def index() -> Dict[str, str]:
    return {"message": "hello amigo :-)"}

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
