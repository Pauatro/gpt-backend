from enum import Enum
from pydantic import BaseModel

class PostRequestSchema(BaseModel):
    data: str
