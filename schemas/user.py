# Datetime
from datetime import datetime

# Application
from base import BaseSchema  # Base


# Profile Schema
class ProfileSchema(BaseSchema):
    id: int
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime
