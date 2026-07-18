# FastAPI
from fastapi import APIRouter, Depends, HTTPException

# SQLAlchemy
from sqlalchemy.orm import Session

# Application
from dependencies.db import get_db  # Get DB
from security.password import hash_password, verify_password  # Password
from security.token import create_token  # Token
from schemas.auth import SigninSchema, SignupSchema, TokenSchema  # Schemas
from models import User

# Router
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/signup", response_model=TokenSchema)
async def signup(data: SignupSchema, db: Session = Depends(get_db)):
    email_exists = db.query(User).where(User.email == data.email).first()

    if email_exists:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    username_exists = db.query(User).where(User.username == data.username).first()

    if username_exists:
        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )

    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.username,
        email=data.email,
        password=hash_password(data.password),
    )

    db.add(user)

    db.commit()
    db.refresh(user)

    access_token = create_token(user.id)

    return TokenSchema(
        access_token=access_token,
        token_type="bearer",
    )


@router.post("/signin", response_model=TokenSchema)
async def signin(data: SigninSchema, db: Session = Depends(get_db)):
    user = db.query(User).where(User.email == data.email).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_token(user.id)

    return TokenSchema(
        access_token=access_token,
        token_type="bearer",
    )
