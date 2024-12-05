import uuid
from typing import List
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

from app.models.medias import Media, MediaPublic

class PostBase(SQLModel):
    content: str = Field(max_length=2200)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None

class Post(PostBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    medias: List[Media] = Relationship(back_populates="post")

class PostCreate(SQLModel):
    content: str = Field(max_length=2200)
    user_id: uuid.UUID

class PostUpdate(SQLModel):
    content: str | None = Field(default=None, max_length=2200)

class PostPublic(PostBase):
    id: uuid.UUID
    user_id: uuid.UUID
    medias: List[MediaPublic]
