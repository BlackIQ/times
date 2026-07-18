# Datetime
from datetime import datetime

# Application
from base import BaseSchema  # Base
from schemas.user import UserProfileSchema  # User Schema


# Create Note
class NoteCreate(BaseSchema):
    slug: str
    title: str
    content: str


# Update Note
class NoteUpdate(BaseSchema):
    slug: str | None = None
    title: str | None = None
    content: str | None = None


# Read Note
class NoteRead(NoteCreate):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: UserProfileSchema
