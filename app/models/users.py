import uuid

from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    bio: str = Field(default="Hello!, I'm new here")
    profile_picture: str | None = None
    is_private: bool = Field(default=False)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class UserCreate(SQLModel):
    email: str
    username: str = Field(min_length=3, max_length=50)

class UserUpdate(SQLModel):
    email: str | None = None
    username: str | None = Field(default=None, min_length=3, max_length=50)
    bio: str | None = None
    profile_picture: str | None = None
    is_private: bool | None = None

class UserPublic(UserBase):
    id: uuid.UUID
