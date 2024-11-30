from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

from models.users import User, UserPublic, UserCreate
from database import engine

router = APIRouter()

@router.post("/users", response_model=UserPublic)
def create_user(user: UserCreate) -> User:
    with Session(engine) as session:
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

@router.get("/users", response_model=Sequence[UserPublic])
def read_users() -> Sequence[User]:
    with Session(engine) as session:
        return session.exec(select(User)).all()

@router.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: UUID) -> User:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
