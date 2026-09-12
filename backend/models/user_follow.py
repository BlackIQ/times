# Libs
import uuid  # UUID

from sqlalchemy import Uuid, ForeignKey, CheckConstraint  # SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column  # SQLAlchemy ORM

# Application
from base.model import BaseModel  # Base: Model


# User-Follow Model
class UserFollow(BaseModel):
    __tablename__ = "user_follows"

    follower_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    following_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    __table_args__ = (
        CheckConstraint(
            "follower_id != following_id",
            name="ck_user_follows_no_self_follow",
        ),
    )
