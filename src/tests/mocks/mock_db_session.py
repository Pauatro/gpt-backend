import os
from typing import Type
from tests.mocks.class_fixture import patch_class_key


class MockDBSession:
    def execute(statement) -> [Type]:
        return

    def add(input: Type):
        return

    def commit():
        return

    def refresh(input: Type) -> Type:
        return input


def get_patched_db_session(mocker, var: str, value):
    return patch_class_key(
        mocker,
        f"tests.mocks.mock_db_session.MockDBSession.{var}",
        value,
    )


class MockDBReturn:
    def __new__(self, input):
        return self

    def first():
        return


def get_patched_db_return(mocker, var: str, value):
    return patch_class_key(
        mocker,
        f"tests.mocks.mock_db_session.MockDBReturn.{var}",
        value,
    )
