# SQLAlchemy
from sqlalchemy import Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# UUID
import uuid

# Application
from base import BaseModel  # Base


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
