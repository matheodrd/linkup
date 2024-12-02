import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./dev.db"
    )
    MEDIA_DIR: str = os.getenv(
        "MEDIA_DIR", "static/media"
    )

settings = Settings()
