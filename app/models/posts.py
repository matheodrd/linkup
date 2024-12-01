import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field

class PostBase(SQLModel):
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None

class Post(PostBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)

class PostCreate(SQLModel):
    content: str
    user_id: uuid.UUID

class PostUpdate(SQLModel):
    content: str | None = None
    updated_at: datetime = Field(default_factory=datetime.now)

class PostPublic(PostBase):
    id: uuid.UUID
    user_id: uuid.UUID
