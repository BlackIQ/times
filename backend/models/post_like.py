# Libs
import uuid  # UUID

from sqlalchemy import Uuid, ForeignKey  # SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column  # SQLAlchemy ORM

# Application
from base.model import BaseModel  # Base: Model


# Post-Like Model
class PostLike(BaseModel):
    __tablename__ = "post_likes"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    post_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
    )
