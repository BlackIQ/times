# Datetime
from datetime import datetime

# Application
from base import BaseSchema  # Base
from schemas.user import UserProfileSchema  # User Schema


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
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: UserProfileSchema
