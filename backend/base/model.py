# SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Application
from base.mixins import TimestampMixin, SoftDeleteMixin  # Mixins


# Base Class: Model
class BaseModel(TimestampMixin, SoftDeleteMixin, DeclarativeBase):
    pass
