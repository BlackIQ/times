# Libs
from fastapi import APIRouter, Depends, HTTPException  # FastAPI
from sqlalchemy.orm import Session  # SQLAlchemy ORM

# Application
from dependencies.database import get_db  # Dependencies: Database
from dependencies.auth import get_current_user  # Dependencies: Current User
from security.password import hash_password, verify_password  # Security: Password
from models.user import User  # Models: User
from schemas.user import (
    UserProfileSchema,
    ChangeProfileSchema,
    ChangePasswordSchema,
    ChangeEmailSchema,
)  # Schemas: User

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
    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=409,
            detail="New passwords are not same",
        )

    if not verify_password(data.current_password, user.password):
        raise HTTPException(
            status_code=409,
            detail="Current password is wrong",
        )

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
    if user.email == data.email:
        raise HTTPException(
            status_code=409,
            detail="New email is same as your current email",
        )

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
