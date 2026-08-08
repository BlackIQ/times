# SQLAlchemy
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

# UUID
import uuid

# Application
from base import BaseModel  # Base


# User Model
class User(BaseModel):
    __tablename__ = "users"

    # Columns
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    username: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        nullable=True,
    )
    bio: Mapped[str] = mapped_column(
        nullable=True,
    )

    # Relationships
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",
    )
