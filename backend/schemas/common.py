# Application
from base import BaseSchema  # Base


# Token Schema
class TokenSchema(BaseSchema):
    access_token: str
    token_type: str


# Message Schema
class MessageSchema(BaseSchema):
    message: str
