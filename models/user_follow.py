# SQLAlchemy
from sqlalchemy import Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# UUID
import uuid

# Application
from base import BaseModel  # Base


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
