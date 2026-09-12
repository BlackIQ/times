# Libs
import uuid  # UUID

from sqlalchemy import Uuid, ForeignKey  # SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column  # SQLAlchemy ORM

# Application
from base.model import BaseModel  # Base: Model


# Comment-Like Model
class CommentLike(BaseModel):
    __tablename__ = "comment_likes"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    comment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("comments.id", ondelete="CASCADE"),
        primary_key=True,
    )
