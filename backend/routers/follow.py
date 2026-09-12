# Libs
import uuid  # UUID

from fastapi import APIRouter, Depends, HTTPException, status  # FastAPI
from sqlalchemy.orm import Session  # SQLAlchemy ORM

# Application
from dependencies.database import get_db  # Dependencies: Database
from dependencies.auth import get_current_user  # Dependencies: Current User
from models.user_follow import UserFollow  # Models: User-Follow
from models.user import User  # Models: User

# Router
router = APIRouter(
    prefix="/users",
    tags=["Follow"],
)


@router.post("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def follow_user(
    user_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target_user = db.query(User).where(User.id == user_id).one_or_none()

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if target_user.id == user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You can not follow yourself",
        )

    existing_follow = (
        db.query(UserFollow)
        .where(
            UserFollow.follower_id == user.id,
            UserFollow.following_id == target_user.id,
        )
        .one_or_none()
    )

    if existing_follow:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already followed",
        )

    follow = UserFollow(
        follower_id=user.id,
        following_id=target_user.id,
    )

    db.add(follow)
    db.commit()

    return None


@router.delete("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(
    user_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    follow = (
        db.query(UserFollow)
        .where(
            UserFollow.follower_id == user.id,
            UserFollow.following_id == user_id,
        )
        .one_or_none()
    )

    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow relationship not found",
        )

    db.delete(follow)
    db.commit()

    return None
