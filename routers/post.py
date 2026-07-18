# FastAPI
from fastapi import APIRouter, Depends, HTTPException

# SQLAlchemy
from sqlalchemy.orm import Session

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
async def all_posts(user_id: int, db: Session = Depends(get_db)):
    posts = db.query(Post).where(Post.user_id == user_id).all()

    return posts


@router.post("/new", response_model=PostRead)
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


@router.get("/{post_slug}", response_model=PostRead)
async def single_post(post_slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).where(Post.slug == post_slug).one_or_none()

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return post


@router.patch("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.get(Post, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if post.user_id != user.id:
        raise HTTPException(
            status_code=400,
            detail="You can not change another one posts",
        )

    slug_exists = db.query(Post).where(Post.slug == post_data.slug).first()
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
