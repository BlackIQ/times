# Libs
from datetime import datetime  # Datetime

from sqlalchemy import DateTime, func  # SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column  # SQLAlchemy ORM


# Base Class: Timestamp
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# Base Class: Soft delete
class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True,
    )

    @classmethod
    def active(cls):
        return cls.deleted_at.is_(None)
