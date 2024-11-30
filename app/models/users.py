import uuid

from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: uuid.UUID

class UserUpdate(SQLModel):
    email: str | None = None
    username: str | None = None

class UserDelete(UserBase):
    id: uuid.UUID
