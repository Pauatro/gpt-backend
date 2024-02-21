import pytest
import users.services.users as services
import users.services.exceptions as exceptions
from users.services.authentication import get_password_hash
import users.services.schemas as user_schemas
from tests.mocks.mock_db_session import (
    MockDBSession,
    MockDBReturn,
    get_patched_db_session,
    get_patched_db_return,
)
from tests.mocks.users import get_mock_user

mock_username = "username"
mock_password = "password"


@pytest.fixture
def mock_get_user_happy_path(mocker):

    def mock_get_user_in_list():
        return [get_mock_user(mock_username, mock_password)]

    first_mock = get_patched_db_return(mocker, "first", mock_get_user_in_list)
    execute_mock = get_patched_db_session(mocker, "execute", MockDBReturn)

    return first_mock, execute_mock


def test_get_user_by_username_happy_path(mock_get_user_happy_path):
    mock_session = MockDBSession()
    user = services.get_user_by_username(mock_username, mock_session)

    mock_user_first, mock_user_execute = mock_get_user_happy_path
    mock_user_first.assert_called_once()
    mock_user_execute.assert_called_once()

    assert user.username == mock_username


@pytest.fixture
def mock_get_user_fails(mocker):
    def mock_none():
        return []

    first_mock = get_patched_db_return(mocker, "first", mock_none)
    execute_mock = get_patched_db_session(mocker, "execute", MockDBReturn)

    return first_mock, execute_mock


def test_get_user_by_username_fails(mock_get_user_fails):
    mock_session = MockDBSession()

    with pytest.raises(exceptions.UserNotFoundException) as error:
        services.get_user_by_username(mock_username, mock_session)

    mock_user_first, mock_user_execute = mock_get_user_fails
    mock_user_first.assert_called_once()
    mock_user_execute.assert_called_once()


@pytest.fixture
def mock_add_user_happy_path(mocker):

    def mock_refresh_user(user):
        return get_mock_user(mock_username, mock_password)

    add_mock = get_patched_db_session(mocker, "add", MockDBSession.add)
    commit_mock = get_patched_db_session(mocker, "commit", MockDBSession.commit)
    refresh_mock = get_patched_db_session(mocker, "refresh", mock_refresh_user)

    return add_mock, commit_mock, refresh_mock


def test_create_user_happy_path(mock_get_user_fails, mock_add_user_happy_path):
    mock_session = MockDBSession()
    mock_create_user = user_schemas.CreateUser(
        username=mock_username, hashed_password=get_password_hash(mock_password)
    )

    user = services.create_user(mock_create_user, mock_session)

    mock_user_first, mock_user_execute = mock_get_user_fails
    mock_user_first.assert_called_once()
    mock_user_execute.assert_called_once()

    add_mock, commit_mock, refresh_mock = mock_add_user_happy_path

    add_mock.assert_called_once()
    commit_mock.assert_called_once()
    refresh_mock.assert_called_once()

    assert mock_create_user.username == user.username


@pytest.fixture
def mock_add_user_happy_path(mocker):

    def mock_refresh_user(user):
        return get_mock_user(mock_username, mock_password)

    add_mock = get_patched_db_session(mocker, "add", MockDBSession.add)
    commit_mock = get_patched_db_session(mocker, "commit", MockDBSession.commit)
    refresh_mock = get_patched_db_session(mocker, "refresh", mock_refresh_user)

    return add_mock, commit_mock, refresh_mock


def test_create_user_fails(mock_get_user_happy_path, mock_add_user_happy_path):
    mock_session = MockDBSession()
    mock_create_user = user_schemas.CreateUser(
        username=mock_username, hashed_password=get_password_hash(mock_password)
    )
    with pytest.raises(exceptions.UserAlreadyExistsException):
        user = services.create_user(mock_create_user, mock_session)
        assert not user

    mock_user_first, mock_user_execute = mock_get_user_happy_path
    mock_user_first.assert_called_once()
    mock_user_execute.assert_called_once()

    add_mock, commit_mock, refresh_mock = mock_add_user_happy_path

    assert not add_mock.called
    assert not commit_mock.called
    assert not refresh_mock.called


def test_authenticate_user_fails():
    mock_user = get_mock_user()
    wrong_password = "wrong"
    with pytest.raises(exceptions.IncorrectUsernameOrPasswordException):
        services.authenticate_user(mock_user, wrong_password)


def test_authenticate_user_happy_path():
    mock_user = get_mock_user()
    user = services.authenticate_user(mock_user, mock_password)
    assert user
