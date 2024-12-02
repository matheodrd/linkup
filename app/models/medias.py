from typing import Literal
import uuid

from sqlmodel import SQLModel, Field

SupportedTypes = Literal[
    "image/jpeg",
    "image/png",
    "image/gif",
    "video/h264",
    "video/mp4",
    "video/x-msvideo",
    "video/quicktime",
]

class MediaBase(SQLModel):
    media_url: str = Field(index=True, unique=True)
    media_type: SupportedTypes

class Media(MediaBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    post_id: uuid.UUID = Field(foreign_key="post.id", nullable=False)

class MediaCreate(SQLModel):
    post_id: uuid.UUID
    media_url: str
    media_type: SupportedTypes

class MediaPublic(MediaBase):
    id: uuid.UUID
    post_id: uuid.UUID
