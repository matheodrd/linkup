from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session

from models.posts import (
    Post,
    PostCreate,
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
