from fastapi import APIRouter
from sqlmodel import Session

from models.users import User, UserRead, UserCreate
from database import engine

router = APIRouter()

@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate) -> User:
    with Session(engine) as session:
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
