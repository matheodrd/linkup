from typing import Dict

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Link Up")

@app.get("/")
async def index() -> Dict[str, str]:
    return {"message": "hello amigo :-)"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
