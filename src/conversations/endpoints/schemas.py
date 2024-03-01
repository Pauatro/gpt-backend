from pydantic import BaseModel
from conversations.services.schemas import Conversation

class CreateConversationRequestBody(BaseModel):
    request: str


class CreateConversationResponseBody(BaseModel):
    conversation: Conversation