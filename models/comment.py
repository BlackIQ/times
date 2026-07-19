# annotations
from __future__ import annotations

# SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Application
from base import BaseModel  # Base


# Comment Model
class Comment(BaseModel):
    __tablename__ = "comments"

    # Columns
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    content: Mapped[str] = mapped_column(
        nullable=False,
    )

    # Foreign Keys
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"),
        index=True,
        nullable=False,
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id"),
        index=True,
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="comments",
    )
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments",
    )
    parent: Mapped[Comment | None] = relationship(
        "Comment",
        remote_side="Comment.id",
        back_populates="replies",
    )
    sub_comments: Mapped[list[Comment]] = relationship(
        "Comment",
        back_populates="parent",
    )
