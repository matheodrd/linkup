"""
This file contains models for the `User` and `Profile` tables.
They are in the same file to avoid circular imports. They are very tightly related.
"""
from __future__ import annotations
import uuid

from sqlmodel import SQLModel, Field, Relationship

################
##### USER #####

class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # profile will be None for an instant before the creation of the profile
    profile: Profile | None = Relationship(back_populates="user")

class UserCreate(UserBase):
    pass

class UserUpdate(SQLModel):
    email: str | None = None
    username: str | None = None

class UserPublic(UserBase):
    id: uuid.UUID

###################
##### PROFILE #####

class ProfileBase(SQLModel):
    bio: str = Field(default="Hello!, I'm new here")
    profile_picture: str | None = None
    is_private: bool = Field(default=False)

class Profile(ProfileBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    user: User = Relationship(back_populates="profile")

class ProfileUpdate(SQLModel):
    bio: str | None = None
    profile_picture: str | None = None
    is_private: bool | None = None

class ProfilePublic(ProfileBase):
    id: uuid.UUID
    user_id: uuid.UUID
