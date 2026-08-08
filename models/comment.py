# annotations
from __future__ import annotations

# SQLAlchemy
from sqlalchemy import Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# UUID
import uuid

# Application
from base import BaseModel  # Base


# Comment Model
class Comment(BaseModel):
    __tablename__ = "comments"

    # Columns
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    content: Mapped[str] = mapped_column(
        nullable=False,
    )

    # Foreign Keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )
    post_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("posts.id"),
        index=True,
        nullable=False,
    )
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
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
        back_populates="sub_comments",
    )
    sub_comments: Mapped[list[Comment]] = relationship(
        "Comment",
        back_populates="parent",
    )

    liked_by: Mapped[list["User"]] = relationship(
        "User",
        secondary="comment_likes",
        back_populates="liked_comments",
    )
