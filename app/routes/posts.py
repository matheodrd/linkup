from typing import Sequence, List
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, UploadFile, Form
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from services.storage import get_storage_provider
from models.posts import (
    Post,
    PostCreate,
    PostPublic,
)
from models.users import User
from models.medias import SupportedTypes, Media, MediaPublic
from database import engine

router = APIRouter()
storage_provider = get_storage_provider()

@router.post("/posts", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
async def create_post(
    content: str = Form(...),
    user_id: UUID = Form(...),
    files: List[UploadFile] = Form(...),
) -> Post:
    post = PostCreate(content=content, user_id=user_id)

    with Session(engine) as session:
        if not session.get(User, post.user_id):
            raise HTTPException(status_code=404, detail="User not found")

        db_post = Post.model_validate(post)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)

        medias = []
        for file in files:
            if file.content_type not in SupportedTypes.__args__:
                raise HTTPException(status_code=400, detail="Unsupported media type")
            media_url = await storage_provider.save_file(file)
            new_media = Media(
                post_id=db_post.id,
                media_url=media_url,
                media_type=file.content_type,
            )
            session.add(new_media)
            medias.append(new_media)
        session.commit()

        db_post.medias = medias
        return db_post

@router.get("/posts", response_model=Sequence[PostPublic])
def read_posts() -> Sequence[PostPublic]:
    with Session(engine) as session:
        posts = session.exec(select(Post)).all()

        return [
            PostPublic(
                **post.model_dump(),
                medias=[MediaPublic(**media.model_dump()) for media in post.medias],
            )
            for post in posts
        ]

@router.get("/posts/{post_id}", response_model=PostPublic)
def read_post(post_id: UUID) -> PostPublic:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        return PostPublic(
            **post.model_dump(),
            medias=[MediaPublic(**media.model_dump()) for media in post.medias],
        )


from fastapi import UploadFile, Form
from typing import List, Optional

from fastapi import Form, File

@router.patch("/posts/{post_id}", response_model=PostPublic)
async def update_post(
    post_id: UUID,
    content: Optional[str] = Form(None),  # Supports form-urlencoded content
    files: Optional[List[UploadFile]] = File(None),  # For file uploads
) -> PostPublic:
    with Session(engine) as session:
        # Fetch the post
        db_post = session.get(Post, post_id)
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")

        # Update content if provided
        if content is not None:
            db_post.content = content
        db_post.updated_at = datetime.now()

        # Process new media files if provided
        new_medias = []
        if files:
            for file in files:
                if file.content_type not in SupportedTypes.__args__:
                    raise HTTPException(status_code=400, detail="Unsupported media type")

                # Save the file and create a new Media object
                media_url = await storage_provider.save_file(file)
                new_media = Media(
                    post_id=db_post.id,
                    media_url=media_url,
                    media_type=file.content_type,
                )
                session.add(new_media)
                new_medias.append(new_media)

        # Commit changes to the database
        session.add(db_post)
        session.commit()

        # Refresh the post instance to include the new media
        session.refresh(db_post)

        # Convert related Media to MediaPublic for response
        return PostPublic(
            **db_post.model_dump(),
            medias=[MediaPublic(**media.model_dump()) for media in db_post.medias],
        )

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: UUID) -> None:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        session.delete(post)
        session.commit()
