# JWT
import jwt
from jwt.exceptions import PyJWTError

# FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# SQLAlchemy
from sqlalchemy.orm import Session

# UUID
import uuid

# Application
from core.settings import settings  # Settings
from dependencies.database import get_db  # Depenencies
from models import User  # Models

# Secret and Algorithm
SECRET = settings.secret
ALGORITHM = settings.algorithm

# OAuth Schema
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/auth/signin")

# 401 Execption
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token",
    headers={"WWW-Authenticate": "Bearer"},
)


# Get Current User
def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
):
    try:
        # Decode JWT
        payload = jwt.decode(jwt=token, key=SECRET, algorithms=ALGORITHM)
    except PyJWTError:
        raise credentials_exception

    # User ID from payload
    user_id: uuid.UUID | None = payload.get("sub")

    if user_id == None:
        raise credentials_exception

    # Get User from DB
    user = db.get(User, user_id)

    # User is not found
    if user is None:
        raise credentials_exception

    return user
