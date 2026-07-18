# Application
from base import BaseSchema  # Base


# Signin Schema
class SigninSchema(BaseSchema):
    email: str
    password: str


# Signup Schema
class SignupSchema(BaseSchema):
    email: str
    username: str
    password: str
    confirm_password: str
    first_name: str | None = None
    last_name: str | None = None


# Token Schema
class TokenSchema(BaseSchema):
    access_token: str
    token_type: str
