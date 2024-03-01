import pytest
import conversations.services.conversations as services
import conversations.services.exceptions as exceptions
import conversations.services.schemas as conversation_schemas
from tests.mocks.mock_db_session import (
    MockDBSession,
    get_patched_db_session,
)
from tests.mocks.conversations import get_mock_conversation

## Tests should be extended once we get the model working and it's plugged in

mock_user_id = "baf2a7cf-1805-4c7f-8187-77ac1d8219d4"
mock_request = "request"
mock_title = "temporary title"


@pytest.fixture
def mock_add_conversation_happy_path(mocker):

    def mock_refresh_conversation(input):
        return get_mock_conversation(
            user_id=mock_user_id,
            title=mock_title,
        )

    add_mock = get_patched_db_session(mocker, "add", MockDBSession.add)
    commit_mock = get_patched_db_session(mocker, "commit", MockDBSession.commit)
    refresh_mock = get_patched_db_session(mocker, "refresh", mock_refresh_conversation)

    return add_mock, commit_mock, refresh_mock


def test_create_conversation_happy_path(mock_add_conversation_happy_path):
    mock_session = MockDBSession()
    conversation = services.create_conversation(
        user_id=mock_user_id,
        request=mock_request,
        session=mock_session,
    )
    print(conversation.iterations)

    add_mock, commit_mock, refresh_mock = mock_add_conversation_happy_path
    add_mock.assert_called()
    commit_mock.assert_called()
    refresh_mock.assert_called()
    assert conversation.user_id == mock_user_id
    assert conversation.user_id == mock_user_id
