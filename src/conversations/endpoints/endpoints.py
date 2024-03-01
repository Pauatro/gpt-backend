from fastapi import APIRouter, Depends
from shared.settings import Settings
from conversations.endpoints.schemas import (
    CreateConversationRequestBody,
    CreateConversationResponseBody,
)
from shared.endpoints.exceptions import (
    InternalServerHttpException,
)
from users.services.users import get_current_user
from conversations.services.conversations import create_conversation

router = APIRouter()
app_settings = Settings()


@router.post("/conversations")
async def create_conversation_with_request(
    form_data: CreateConversationRequestBody,
    user: str = Depends(get_current_user),
) -> CreateConversationResponseBody:
    try:
        conversation = create_conversation(user_id=user.id, request=form_data.request)
        return CreateConversationResponseBody(conversation=conversation)
    except:
        raise InternalServerHttpException()
    
