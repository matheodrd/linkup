from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from models.users import (
    User,
    UserPublic,
    UserCreate,
    UserUpdate,
)
from models.posts import Post, PostPublic
from database import engine

router = APIRouter()

@router.post("/users", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> User:
    with Session(engine) as session:
        # Check username and e-mail address uniqueness
        if session.exec(select(User).where(User.email == user.email)).first():
            raise HTTPException(status_code=400, detail="Email already in use")
        if session.exec(select(User).where(User.username == user.username)).first():
            raise HTTPException(status_code=400, detail="Username already in use")

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

@router.get("/users/{user_id}/posts", response_model=Sequence[PostPublic])
def read_user_posts(user_id: UUID) -> Sequence[Post]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        statement = select(Post).where(Post.user_id == user_id)
        user_posts = session.exec(statement).all()

        return user_posts

@router.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: UUID, user: UserUpdate) -> User:
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check username and e-mail address uniqueness
        if user.email and session.exec(select(User).where(User.email == user.email, User.id != user_id)).first():
            raise HTTPException(status_code=400, detail="Email already in use")
        if user.username and session.exec(select(User).where(User.username == user.username, User.id != user_id)).first():
            raise HTTPException(status_code=400, detail="Username already in use")

        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID) -> None:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
