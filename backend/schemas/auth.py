# Application
from base.schema import BaseSchema  # Base: Schema


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
    first_name: str
    last_name: str | None = None
