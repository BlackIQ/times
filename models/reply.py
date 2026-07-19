# annotations
from __future__ import annotations

# SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Application
from base import BaseModel  # Base


# Reply Model
class Reply(BaseModel):
    __tablename__ = "replies"

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
    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id"),
        index=True,
        nullable=False,
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("replies.id"),
        index=True,
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="replies",
    )
    note: Mapped["Note"] = relationship(
        "Note",
        back_populates="replies",
    )
    parent: Mapped[Reply | None] = relationship(
        "Reply",
        remote_side="Reply.id",
        back_populates="replies",
    )
    sub_reply: Mapped[list[Reply]] = relationship(
        "Reply",
        back_populates="parent",
    )
