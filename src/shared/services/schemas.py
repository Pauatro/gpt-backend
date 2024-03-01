from pydantic import BaseModel, UUID4
from datetime import datetime


class EntityBase(BaseModel):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
