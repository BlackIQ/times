# Pydantic
from pydantic import BaseModel, ConfigDict


# Base Class: Schema
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
