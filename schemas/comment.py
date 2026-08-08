# Datetime
from datetime import datetime

# UUID
import uuid

# Application
from base import BaseSchema  # Base
from schemas.user import UserProfileSchema  # User Schema


# Comment Create
class CommentCreate(BaseSchema):
    content: str

    post_id: uuid.UUID
    parent_id: uuid.UUID | None = None


# Update Comment
class CommentUpdate(BaseSchema):
    content: str


# Comment Read
class CommentRead(BaseSchema):
    id: uuid.UUID

    content: str

    post_id: uuid.UUID
    parent_id: uuid.UUID | None
    user_id: uuid.UUID

    created_at: datetime
    updated_at: datetime

    user: UserProfileSchema

    # count_likes: int
    # count_comments: int
