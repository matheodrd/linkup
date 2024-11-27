"""This should later be replaced by migrations using Alembic (see issue #9)"""
from sqlmodel import SQLModel
from database import engine

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
