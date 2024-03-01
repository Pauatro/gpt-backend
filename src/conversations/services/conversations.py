from pydantic import UUID4
from shared.database import get_db_session
from shared.logging.logging import get_logger
from conversations.data.models import ConversationModel, IterationModel
from conversations.services.exceptions import (
    UnexpectedConversationException,
    UnexpectedIterationException,
)

MOCK_TITLE = "temporary title"
MOCK_RESPONSE = "This is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./tThis is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./tThis is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./tThis is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./tThis is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./tThis is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./tThis is a mock response from the model, use it temporarily to work with the data structure and check that the text can be displayed properly./t"


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
        new_iteration = IterationModel(
            conversation_id=new_conversation.id,
            request=request,
            response=MOCK_RESPONSE,
        )

        session.add(new_iteration)
        session.commit()
        session.refresh(new_conversation)
        session.refresh(new_iteration)
        logger.info(
            f"New iteration was created with id {new_iteration.id}, request {new_iteration.request} and response {new_iteration.response}"
        )

        return new_conversation
    except Exception as error:
        logger.error(error)
        raise UnexpectedIterationException(error)
