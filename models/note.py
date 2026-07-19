# SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Application
from base import BaseModel  # Base


# Note Model
class Note(BaseModel):
    __tablename__ = "notes"

    # Columns
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    slug: Mapped[str] = mapped_column(
        unique=True,
        index=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        nullable=False,
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

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="notes",
    )
    replies: Mapped[list["Reply"]] = relationship(
        "Comment",
        back_populates="note",
    )
