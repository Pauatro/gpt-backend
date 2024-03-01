from pydantic import UUID4
from sqlalchemy import select
from shared.database import get_db_session
from shared.logging.logging import get_logger
from shared.services.exceptions import UnauthorizedException
from conversations.data.models import ConversationModel, IterationModel
from conversations.services.exceptions import (
    UnexpectedConversationException,
    UnexpectedIterationException,
    ConversationNotFoundException,
)
from conversations.services.schemas import Conversation

MOCK_TITLE = "temporary title"
MOCK_RESPONSE = "This is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./tThis is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./tThis is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./tThis is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./tThis is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./tThis is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./tThis is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./t"


def create_iteration(
    conversation_id: UUID4,
    request: str,
    session=get_db_session(),
    logger=get_logger(),
):
    try:
        new_iteration = IterationModel(
            conversation_id=conversation_id,
            request=request,
            response=MOCK_RESPONSE,
        )

        session.add(new_iteration)
        session.commit()
        session.refresh(new_iteration)
        logger.info(
            f"New iteration was created with id {new_iteration.id}, request {new_iteration.request} and response {new_iteration.response}"
        )

        return new_iteration
    except Exception as error:
        logger.error(error)
        raise UnexpectedIterationException(error)


def create_conversation(
    user_id: UUID4,
    request: str,
    session=get_db_session(),
    logger=get_logger(),
):
    new_conversation = ConversationModel(
        user_id=user_id,
        title=MOCK_TITLE,
    )
    try:
        session.add(new_conversation)
        session.commit()
        session.refresh(new_conversation)
        logger.info(
            f"New conversation was created with id {new_conversation.id} and title {new_conversation.title}"
        )
    except Exception as error:
        logger.error(error)
        raise UnexpectedConversationException(error)

    try:
        create_iteration(
            conversation_id=new_conversation.id,
            request=request,
            session=session,
            logger=logger,
        )
        session.refresh(new_conversation)

        return new_conversation
    except Exception as error:
        logger.error(error)
        raise UnexpectedIterationException(error)


def get_conversations_by_user(
    user_id: UUID4,
    session=get_db_session(),
    logger=get_logger(),
):
    try:
        statement = select(ConversationModel).where(
            ConversationModel.user_id == user_id
        )
        conversation_list = session.execute(statement).all()
        logger.info(
            f"{len(conversation_list)} conversations have been retrieved for user with id {user_id}"
        )
        return [
            Conversation.model_validate(conversation[0])
            for conversation in conversation_list
        ]
    except Exception as error:
        logger.error(error)
        raise UnexpectedConversationException(error)


def get_conversation_by_id(
    id: UUID4,
    session=get_db_session(),
    logger=get_logger(),
) -> Conversation:
    try:
        statement = select(ConversationModel).where(ConversationModel.id == id)
        conversation = session.execute(statement).first()

        if not conversation:
            logger.error(f"Conversations with id {id} was not found")
            raise ConversationNotFoundException()

        logger.info(f"Conversations with id {id} has been retrieved successfully")
        return Conversation.model_validate(conversation[0])
    except ConversationNotFoundException as exception:
        raise exception
    except Exception as error:
        logger.error(error)
        raise UnexpectedConversationException(error)


def create_conversation_iteration(
    conversation_id: UUID4,
    request: str,
    user_id: UUID4,
    session=get_db_session(),
    logger=get_logger(),
) -> Conversation:
    conversation = None
    try:
        conversation = get_conversation_by_id(conversation_id, session, logger)
        if conversation.user_id != user_id:
            raise UnauthorizedException()
    except Exception as exception:
        raise exception

    try:
        create_iteration(conversation_id, request, session, logger)
        return get_conversation_by_id(conversation_id, session, logger)
    except Exception as error:
        logger.error(error)
        raise UnexpectedIterationException(error)
