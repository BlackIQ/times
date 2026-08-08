# SQLAlchemy
from sqlalchemy import Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# UUID
import uuid

# Application
from base import BaseModel  # Base


# Post Model
class Post(BaseModel):
    __tablename__ = "posts"

    # Columns
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
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
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts",
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
    )
