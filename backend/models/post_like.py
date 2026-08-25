# SQLAlchemy
from sqlalchemy import Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# UUID
import uuid

# Application
from base import BaseModel  # Base


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
