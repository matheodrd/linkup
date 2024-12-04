from typing import Literal, Annotated, TYPE_CHECKING
import uuid

from sqlmodel import SQLModel, Field, Relationship

# This is to make the type checker happy because I'm using a forward reference
if TYPE_CHECKING:
    from models.posts import Post

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
    media_type: Annotated[str, SupportedTypes]

class Media(MediaBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    post_id: uuid.UUID = Field(foreign_key="post.id", nullable=False)
    post: "Post" = Relationship(back_populates="medias")

class MediaCreate(SQLModel):
    post_id: uuid.UUID
    media_url: str
    media_type: Annotated[str, SupportedTypes]

class MediaPublic(MediaBase):
    id: uuid.UUID
    post_id: uuid.UUID
