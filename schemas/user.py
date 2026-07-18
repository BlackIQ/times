# Datetime
from datetime import datetime

# Application
from base import BaseSchema  # Base


# Profile Schema
class UserProfileSchema(BaseSchema):
    id: int
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    created_at: datetime
    updated_at: datetime


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
