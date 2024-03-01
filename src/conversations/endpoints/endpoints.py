from fastapi import APIRouter, Depends
from pydantic import UUID4
from shared.settings import Settings
from conversations.endpoints.schemas import (
    CreateConversationRequestBody,
    CreateConversationResponseBody,
    GetConversationsByUserResponseBody,
    ConversationListReturn,
    ConversationReturn,
    GetConversationByIdResponseBody,
    CreateConversationIterationResponseBody,
    CreateConversationIterationRequestBody,
)
from shared.endpoints.exceptions import (
    InternalServerHttpException,
    UnauthorizedHttpException,
)
from users.services.users import get_current_user
from conversations.services.conversations import (
    create_conversation,
    get_conversations_by_user,
    get_conversation_by_id,
    create_conversation_iteration,
)
from shared.logging.logging import get_logger
from users.services.schemas import User

router = APIRouter()
app_settings = Settings()


@router.post("/conversations")
async def create_conversation_with_request(
    form_data: CreateConversationRequestBody,
    user: User = Depends(get_current_user),
) -> CreateConversationResponseBody:
    try:
        conversation = create_conversation(user_id=user.id, request=form_data.request)
        return CreateConversationResponseBody(conversation=conversation)
    except:
        raise InternalServerHttpException()


@router.get("/conversations/user")
async def get_conversations_by_user_request(
    user: User = Depends(get_current_user),
    logger=Depends(get_logger),
) -> GetConversationsByUserResponseBody:
    try:
        conversations_list = get_conversations_by_user(user_id=user.id)
        return GetConversationsByUserResponseBody(
            conversations=[
                ConversationListReturn(**conversation.model_dump())
                for conversation in conversations_list
            ]
        )
    except Exception as error:
        logger.error(error)
        raise InternalServerHttpException()


@router.get("/conversations/{id}")
async def retrieve_conversation_by_id(
    id: UUID4,
    user: User = Depends(get_current_user),
    logger=Depends(get_logger),
) -> GetConversationByIdResponseBody:
    try:
        conversation = get_conversation_by_id(id=id)

        if conversation.user_id != user.id:
            raise UnauthorizedHttpException()

        return GetConversationByIdResponseBody(
            conversation=ConversationReturn(**conversation.model_dump())
        )
    except UnauthorizedHttpException as exception:
        logger.info(error)
        raise exception
    except Exception as error:
        logger.error(error)
        raise InternalServerHttpException()


@router.post("/conversations/{id}/iterations")
async def create_iteration_with_request(
    form_data: CreateConversationIterationRequestBody,
    id: UUID4,
    user: User = Depends(get_current_user),
) -> CreateConversationIterationResponseBody:
    try:
        conversation = create_conversation_iteration(
            conversation_id=id,
            request=form_data.request,
            user_id=user.id,
        )
        return CreateConversationIterationResponseBody(
            conversation=ConversationReturn(**conversation.model_dump())
        )
    except:
        raise InternalServerHttpException()
