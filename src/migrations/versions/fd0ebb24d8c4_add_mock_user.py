"""add mock users

Revision ID: fd0ebb24d8c4
Revises: 
Create Date: 2024-02-28 21:29:17.208929

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from passlib.context import CryptContext

# revision identifiers, used by Alembic.
revision: str = "fd0ebb24d8c4"
down_revision: Union[str, None] = "fd0ebb24d8c3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

username = "username"
password = "password"
id = "baf2a7cf-1805-4c7f-8187-77ac1d8219d4"


def upgrade() -> None:
    users_table = sa.table(
        "users",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("username", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("hashed_password", sa.VARCHAR(), autoincrement=False, nullable=False),
    )

    op.bulk_insert(
        users_table,
        [
            {
                "id": id,
                "username": username,
                "hashed_password": pwd_context.hash(password),
            },
        ],
    )


def downgrade() -> None:
    op.execute(f"DELETE FROM users WHERE id='{id}'")
