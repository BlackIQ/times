# Datetime
from datetime import datetime

# Application
from base import BaseSchema  # Base
from schemas.user import UserProfileSchema  # User Schema


# Reply Create
class ReplyCreate(BaseSchema):
    content: str
    post_id: int
    parent_id: int | None = None


# Update Reply
class ReplyUpdate(BaseSchema):
    content: str


# Reply Read
class ReplyRead(BaseSchema):
    id: int
    content: str
    post_id: int
    parent_id: int | None
    user_id: int

    created_at: datetime
    updated_at: datetime

    user: UserProfileSchema
