from typing import Sequence, List
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, UploadFile, Form, File
from sqlmodel import Session, select

from app.services.storage import get_storage_provider
from app.models.posts import (
    Post,
    PostCreate,
    PostPublic,
)
from app.models.users import User
from app.models.medias import SupportedTypes, Media, MediaPublic
from app.database import engine

router = APIRouter()
storage_provider = get_storage_provider()

@router.post("/posts", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
async def create_post(
    content: str = Form(...),
    user_id: UUID = Form(...),
    files: List[UploadFile] | None = File(None),
) -> PostPublic:
    post = PostCreate(content=content, user_id=user_id)

    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db_post = Post.model_validate(post)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)

        if files:
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

        session.commit()
        session.refresh(db_post)

        return PostPublic(
            **db_post.model_dump(),
            medias=[MediaPublic(**media.model_dump()) for media in db_post.medias],
        )

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

@router.patch("/posts/{post_id}", response_model=PostPublic)
async def update_post(
    post_id: UUID,
    content: str | None = Form(None),
    files: List[UploadFile] | None = File(None),
) -> PostPublic:
    with Session(engine) as session:
        db_post = session.get(Post, post_id)
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")

        if content is not None:
            db_post.content = content
        db_post.updated_at = datetime.now()

        new_medias = []
        if files:
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
                new_medias.append(new_media)

        session.add(db_post)
        session.commit()
        session.refresh(db_post)

        return PostPublic(
            **db_post.model_dump(),
            medias=[MediaPublic(**media.model_dump()) for media in db_post.medias],
        )

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: UUID) -> None:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        medias = session.exec(select(Media).where(Media.post_id == post_id)).all()
        for media in medias:
            await storage_provider.delete_file(media.media_url)
            session.delete(media)

        session.delete(post)
        session.commit()
