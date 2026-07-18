# Application
from base import BaseSchema  # Base


# Signin Schema
class SigninSchema(BaseSchema):
    email: str
    password: str


# Signup Schema
class SignupSchema(SigninSchema):
    username: str
    first_name: str
    last_name: str


# Token Schema
class TokenSchema(BaseSchema):
    access_token: str
    token_type: str
