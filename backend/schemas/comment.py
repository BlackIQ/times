# Libs
import uuid  # UUID
from datetime import datetime  # Datetime

# Application
from base.schema import BaseSchema  # Base: Schema
from schemas.user import UserPublicProfileSchema  # Schemas: User


# Comment Create
class CommentCreate(BaseSchema):
    content: str

    post_id: uuid.UUID
    parent_id: uuid.UUID | None = None


# Update Comment
class CommentUpdate(BaseSchema):
    content: str | None = None


# Comment Read
class CommentRead(BaseSchema):
    id: uuid.UUID

    content: str

    post_id: uuid.UUID
    parent_id: uuid.UUID | None
    user_id: uuid.UUID

    created_at: datetime
    updated_at: datetime

    user: UserPublicProfileSchema
