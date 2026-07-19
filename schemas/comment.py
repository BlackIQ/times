# Datetime
from datetime import datetime

# Application
from base import BaseSchema  # Base
from schemas.user import UserProfileSchema  # User Schema


# Comment Create
class CommentCreate(BaseSchema):
    content: str
    post_id: int
    parent_id: int | None = None


# Update Comment
class CommentUpdate(BaseSchema):
    content: str


# Comment Read
class CommentRead(BaseSchema):
    id: int
    content: str
    post_id: int
    parent_id: int | None
    user_id: int

    created_at: datetime
    updated_at: datetime

    user: UserProfileSchema
