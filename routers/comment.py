# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status

# SQLAlchemy
from sqlalchemy.orm import Session

# Datetime
from datetime import datetime, timezone

# Application
from dependencies.db import get_db  # Get Database
from dependencies.auth import get_current_user  # Get Current User
from schemas.comment import CommentCreate, CommentUpdate, CommentRead  # Schemas
from models import Comment, User  # Models

# Router
router = APIRouter(
    prefix="/comments",
    tags=["Comment"],
)


@router.get("/user/{user_id}", response_model=list[CommentRead])
async def list_user_comments(
    user_id: int,
    db: Session = Depends(get_db),
):
    comments = (
        db.query(Comment)
        .where(
            Comment.user_id == user_id,
        )
        .all()
    )

    return comments


@router.get("/post/{post_id}", response_model=list[CommentRead])
async def list_post_comments(
    post_id: int,
    db: Session = Depends(get_db),
):
    comments = (
        db.query(Comment)
        .where(
            Comment.post_id == post_id,
            Comment.parent == None,
        )
        .all()
    )

    return comments


@router.get("/childrent/{parent_id}", response_model=list[CommentRead])
async def list_children_comments(
    parent_id: int,
    db: Session = Depends(get_db),
):
    comments = (
        db.query(Comment)
        .where(
            Comment.parent_id == parent_id,
        )
        .all()
    )

    return comments


@router.post("", response_model=CommentRead)
async def create_comment(
    comment: CommentCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_comment = Comment(**comment.model_dump(), user_id=user.id)

    db.add(db_comment)

    db.commit()
    db.refresh(db_comment)

    return db_comment


@router.patch("/{comment_id}", response_model=CommentRead)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comment = (
        db.query(Comment)
        .where(
            Comment.id == comment_id,
            Comment.deleted_at.is_not(None),
        )
        .one_or_none()
    )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    if comment.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can not change another one comments",
        )

    data = comment_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(comment, key, value)

    db.commit()
    db.refresh(comment)

    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comment = (
        db.query(Comment)
        .where(
            Comment.id == comment_id,
            Comment.deleted_at.is_(None),
        )
        .one_or_none()
    )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    if comment.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can not change another one comments",
        )

    comment.content = "[Deleted comment]"
    comment.deleted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(comment)

    return None
