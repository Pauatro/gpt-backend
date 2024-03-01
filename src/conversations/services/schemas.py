from pydantic import BaseModel, UUID4
from typing import List
from shared.services.schemas import EntityBase


class Iteration(EntityBase):
    conversation_id: UUID4
    request: str
    response: str


class Conversation(EntityBase):
    user_id: UUID4
    title: str
    iterations: List[Iteration]


class CreateConversation(BaseModel):
    user_id: UUID4
    title: str


class CreateIteration(BaseModel):
    conversation_id: UUID4
    request: str
    response: str
