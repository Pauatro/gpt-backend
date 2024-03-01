from pydantic import BaseModel, UUID4
from datetime import datetime
from conversations.services.schemas import Conversation
from typing import List


class ConversationListReturn(BaseModel):
    id: UUID4
    title: str
    created_at: datetime


class IterationListReturn(BaseModel):
    id: UUID4
    request: str
    response: str
    created_at: datetime


class ConversationReturn(BaseModel):
    id: UUID4
    title: str
    created_at: datetime
    iterations: List[IterationListReturn]


class GetConversationsByUserResponseBody(BaseModel):
    conversations: List[ConversationListReturn]


class CreateConversationRequestBody(BaseModel):
    request: str


class CreateConversationResponseBody(BaseModel):
    conversation: ConversationReturn


class GetConversationByIdResponseBody(CreateConversationResponseBody):
    pass


class CreateConversationIterationResponseBody(CreateConversationResponseBody):
    pass


class CreateConversationIterationRequestBody(CreateConversationRequestBody):
    pass
