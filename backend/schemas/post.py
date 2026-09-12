# Libs
import uuid  # UUID
from datetime import datetime  # Datetime

# Application
from base.schema import BaseSchema  # Base: Schema
from schemas.user import UserPublicProfileSchema  # Schemas: User


# Create Post
class PostCreate(BaseSchema):
    slug: str
    title: str
    content: str


# Update Post
class PostUpdate(BaseSchema):
    slug: str | None = None
    title: str | None = None
    content: str | None = None


# Read Post
class PostRead(PostCreate):
    id: uuid.UUID

    user_id: uuid.UUID

    created_at: datetime
    updated_at: datetime

    user: UserPublicProfileSchema
