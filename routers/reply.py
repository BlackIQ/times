# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status

# SQLAlchemy
from sqlalchemy.orm import Session

# Datetime
from datetime import datetime, timezone

# Application
from dependencies.db import get_db  # Get Database
from dependencies.auth import get_current_user  # Get Current User
from schemas.reply import ReplyCreate, ReplyUpdate, ReplyRead  # Schemas
from models import Reply, User  # Models

# Router
router = APIRouter(
    prefix="/replies",
    tags=["Reply"],
)


@router.get("/user/{user_id}", response_model=list[ReplyRead])
async def list_user_replies(
    user_id: int,
    db: Session = Depends(get_db),
):
    replies = (
        db.query(Reply)
        .where(
            Reply.user_id == user_id,
        )
        .all()
    )

    return replies


@router.post("", response_model=ReplyRead)
async def create_reply(
    reply: ReplyCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_reply = Reply(**reply.model_dump(), user_id=user.id)

    db.add(db_reply)

    db.commit()
    db.refresh(db_reply)

    return db_reply


@router.patch("/{reply_id}", response_model=ReplyRead)
async def update_reply(
    reply_id: int,
    reply_data: ReplyUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reply = (
        db.query(Reply)
        .where(
            Reply.id == reply_id,
            Reply.deleted_at.is_not(None),
        )
        .one_or_none()
    )

    if not reply:
        raise HTTPException(
            status_code=404,
            detail="Reply not found",
        )

    if reply.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can not change another one replies",
        )

    data = reply_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(reply, key, value)

    db.commit()
    db.refresh(reply)

    return reply


@router.delete("/{reply_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reply(
    reply_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reply = (
        db.query(Reply)
        .where(
            Reply.id == reply_id,
            Reply.deleted_at.is_(None),
        )
        .one_or_none()
    )

    if not reply:
        raise HTTPException(
            status_code=404,
            detail="Reply not found",
        )

    if reply.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can not change another one replies",
        )

    reply.content = "[Deleted reply]"
    reply.deleted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(reply)

    return None
