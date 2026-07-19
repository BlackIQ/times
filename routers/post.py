# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status

# SQLAlchemy
from sqlalchemy.orm import Session

# Datetime
from datetime import datetime, timezone

# Application
from dependencies.db import get_db  # Get Database
from dependencies.auth import get_current_user  # Get Current User
from schemas.post import PostCreate, PostUpdate, PostRead  # Schemas
from models import Post, User  # Models

# Router
router = APIRouter(
    prefix="/posts",
    tags=["Post"],
)


@router.get("/user/{user_id}", response_model=list[PostRead])
async def list_user_posts(
    user_id: int,
    db: Session = Depends(get_db),
):
    posts = (
        db.query(Post)
        .where(
            Post.user_id == user_id,
            Post.deleted_at.is_(None),
        )
        .all()
    )

    return posts


@router.get("/trash", response_model=list[PostRead])
async def list_user_deleted_posts(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    posts = (
        db.query(Post)
        .where(
            Post.user_id == user.id,
            Post.deleted_at.is_not(None),
        )
        .all()
    )

    return posts


@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = (
        db.query(Post)
        .where(
            Post.id == post_id,
            Post.deleted_at.is_(None),
        )
        .one_or_none()
    )

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return post


@router.post("", response_model=PostRead)
async def create_post(
    post: PostCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    slug_exists = db.query(Post).where(Post.slug == post.slug).first()
    if slug_exists:
        raise HTTPException(
            status_code=409,
            detail="Slug already exists",
        )

    db_post = Post(**post.model_dump(), user_id=user.id)

    db.add(db_post)

    db.commit()
    db.refresh(db_post)

    return db_post


@router.patch("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = (
        db.query(Post)
        .where(
            Post.id == post_id,
            Post.deleted_at.is_(None),
        )
        .one_or_none()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if post.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can not change another one posts",
        )

    slug_exists = (
        db.query(Post)
        .where(
            Post.slug == post_data.slug,
            Post.id != post.id,
        )
        .first()
    )
    if slug_exists:
        raise HTTPException(
            status_code=409,
            detail="Slug already exists",
        )

    data = post_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)

    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_post(
    post_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = (
        db.query(Post)
        .where(
            Post.id == post_id,
            Post.deleted_at.is_(None),
        )
        .one_or_none()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if post.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can not change another one posts",
        )

    post.deleted_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(post)

    return None


@router.post("/{post_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_post(
    post_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = (
        db.query(Post)
        .where(
            Post.id == post_id,
            Post.deleted_at.is_not(None),
        )
        .one_or_none()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if post.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can not change another one posts",
        )

    post.deleted_at = None

    db.commit()
    db.refresh(post)

    return None


@router.delete("/{post_id}/force", status_code=status.HTTP_204_NO_CONTENT)
async def hard_delete_post(
    post_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = (
        db.query(Post)
        .where(
            Post.id == post_id,
            Post.deleted_at.is_not(None),
        )
        .one_or_none()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if post.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You can not change another one posts",
        )

    db.delete(post)

    db.commit()

    return None
