from typing import Sequence
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from models.posts import (
    Post,
    PostCreate,
    PostUpdate,
    PostPublic,
)
from models.users import User
from database import engine

router = APIRouter()

@router.post("/posts", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate) -> Post:
    with Session(engine) as session:
        if not session.get(User, post.user_id):
            raise HTTPException(status_code=404, detail="User not found")

        db_post = Post.model_validate(post)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        return db_post

@router.get("/posts", response_model=Sequence[PostPublic])
def read_posts() -> Sequence[Post]:
    with Session(engine) as session:
        return session.exec(select(Post)).all()

@router.get("/posts/{post_id}", response_model=PostPublic)
def read_post(post_id: UUID) -> Post:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

@router.patch("/posts/{post_id}", response_model=PostPublic)
def update_post(post_id: UUID, post: PostUpdate) -> Post:
    with Session(engine) as session:
        db_post = session.get(Post, post_id)
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")

        db_post.updated_at = datetime.now()

        post_data = post.model_dump(exclude_unset=True)
        db_post.sqlmodel_update(post_data)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        return db_post
