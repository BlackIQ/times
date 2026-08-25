# Datetime
from datetime import datetime

# UUID
import uuid

# Application
from base import BaseSchema  # Base


# Public Profile Schema
class UserPublicProfileSchema(BaseSchema):
    id: uuid.UUID

    username: str
    first_name: str
    last_name: str | None = None
    bio: str | None = None

    created_at: datetime
    updated_at: datetime

    # followers_count: int
    # following_count: int


# Profile Schema
class UserProfileSchema(BaseSchema):
    email: str


# Change profile
class ChangeProfileSchema(BaseSchema):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None


# Change email
class ChangeEmailSchema(BaseSchema):
    email: str


# Rest Password
class ChangePasswordSchema(BaseSchema):
    current_password: str
    new_password: str
    confirm_password: str
