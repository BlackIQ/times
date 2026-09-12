# Libs
from sqlalchemy.orm import DeclarativeBase  # SQLAlchemy ORM

# Application
from base.mixins import TimestampMixin, SoftDeleteMixin  # Base: Mixins


# Base Class: Model
class BaseModel(TimestampMixin, SoftDeleteMixin, DeclarativeBase):
    pass
