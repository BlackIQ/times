# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status

# SQLAlchemy
from sqlalchemy.orm import Session

# Datetime
from datetime import datetime, timezone

# UUID
import uuid

# Application
from dependencies.db import get_db  # Get Database
from dependencies.auth import get_current_user  # Get Current User
from schemas.comment import CommentCreate, CommentUpdate, CommentRead  # Comment Schemas
from models import Comment, User, CommentLike  # Models

# Router
router = APIRouter(
    prefix="/comments",
    tags=["Comment"],
)


@router.get("/user/{user_id}", response_model=list[CommentRead])
async def list_user_comments(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    comments = (
        db.query(Comment)
        .where(
            Comment.user_id == user_id,
        )
        .all()
    )

    # for comment in comments:
    #     setattr(comment, "count_likes", len(comment.liked_by))
    #     setattr(comment, "count_comments", len(comment.sub_comments))

    return comments


@router.get("/post/{post_id}", response_model=list[CommentRead])
async def list_post_comments(
    post_id: uuid.UUID,
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
    parent_id: uuid.UUID,
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
    comment_id: uuid.UUID,
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
    comment_id: uuid.UUID,
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


@router.post("/{comment_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def like_comment(
    comment_id: uuid.UUID,
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    existing_like = (
        db.query(CommentLike)
        .where(
            CommentLike.user_id == user.id,
            CommentLike.comment_id == comment.id,
        )
        .one_or_none()
    )

    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Comment already liked",
        )

    like = CommentLike(
        user_id=user.id,
        comment_id=comment.id,
    )

    db.add(like)
    db.commit()

    return None


@router.delete("/{comment_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_comment(
    comment_id: uuid.UUID,
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    like = (
        db.query(CommentLike)
        .where(
            CommentLike.user_id == user.id,
            CommentLike.comment_id == comment.id,
        )
        .one_or_none()
    )

    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Like not found",
        )

    db.delete(like)
    db.commit()

    return None
