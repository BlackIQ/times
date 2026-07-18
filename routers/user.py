# FastAPI
from fastapi import APIRouter, Depends, HTTPException

# SQLAlchemy
from sqlalchemy.orm import Session

# Application
from dependencies.db import get_db  # Get Database
from dependencies.auth import get_current_user  # Get Current User
from security.password import hash_password, verify_password  # Password
from schemas.user import (
    UserProfileSchema,
    ChangeProfileSchema,
    ChangePasswordSchema,
    ChangeEmailSchema,
)  # Schemas
from models import User  # Models

# Router
router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.get("/me", response_model=UserProfileSchema)
async def profile(
    user: User = Depends(get_current_user),
):
    return user


@router.patch("/me", response_model=UserProfileSchema)
async def change_profile(
    data: ChangeProfileSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


@router.patch("/password", response_model=UserProfileSchema)
async def change_password(
    data: ChangePasswordSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check new password is equal to confirm password
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=409, detail="New passwords are not same")

    # Check if current password is right or no
    if not verify_password(data.current_password, user.password):
        raise HTTPException(status_code=409, detail="Current password is wrong")

    # Now confirm is equal to new and user password is same
    new_password_hash = hash_password(data.new_password)

    user.password = new_password_hash

    db.commit()
    db.refresh(user)

    return user


@router.patch("/email", response_model=UserProfileSchema)
async def change_email(
    data: ChangeEmailSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check is it current email
    if user.email == data.email:
        raise HTTPException(
            status_code=409, detail="New email is same as your current email"
        )

    # Check email exists
    email_exists = db.query(User).where(User.email == data.email).first()
    if email_exists:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    user.email = data.email

    db.commit()
    db.refresh(user)

    return user
