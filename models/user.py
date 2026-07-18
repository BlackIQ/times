# SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Application
from base import BaseModel  # Base


# User Model
class User(BaseModel):
    __tablename__ = "users"

    # Columns
    id: Mapped[int] = mapped_column(
        primary_key=True,
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
        nullable=True,
    )
    last_name: Mapped[str] = mapped_column(
        nullable=True,
    )
    bio: Mapped[str] = mapped_column(
        nullable=True,
    )

    # Relationships
    notes: Mapped[list["Note"]] = relationship(
        "Note",
        back_populates="user",
    )
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",
    )
