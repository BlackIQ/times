# Application
from base.schema import BaseSchema  # Base: Schema


# Token Schema
class TokenSchema(BaseSchema):
    access_token: str
    token_type: str


# Message Schema
class MessageSchema(BaseSchema):
    message: str
