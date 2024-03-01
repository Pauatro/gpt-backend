import uuid
from datetime import datetime
from conversations.data.models import ConversationModel, IterationModel
from pydantic import UUID4
from typing import List


def get_mock_iteration(
    request: str = "temporary request",
    response: str = "temporary response",
    conversation_id: UUID4 = "baf2a7cf-1805-4c7f-8187-77ac1d8219d4",
):
    return IterationModel(
        request=request,
        response=response,
        conversation_id=conversation_id,
        id=uuid.uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def get_mock_conversation(
    title: str = "temporary title",
    user_id: UUID4 = "baf2a7cf-1805-4c7f-8187-77ac1d8219d4",
    iterations: List[IterationModel] = [get_mock_iteration()],
):
    return ConversationModel(
        title=title,
        user_id=user_id,
        id=uuid.uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        iterations=iterations,
    )
