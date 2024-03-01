"""add iterations and conversations

Revision ID: 091e5f1bc9ba
Revises: fd0ebb24d8c4
Create Date: 2024-02-29 13:29:24.847091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '091e5f1bc9ba'
down_revision: Union[str, None] = 'fd0ebb24d8c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "conversations",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
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
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.id"), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="conversations_pkey"),
    )
    op.create_index("ix_conversations_id", "conversations", ["id"], unique=False)

    op.create_table(
        "iterations",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
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
        sa.Column("request", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("response", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("conversation_id", sa.UUID(), sa.ForeignKey("conversations.id"), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="iterations_pkey"),
    )
    op.create_index("ix_iterations_id", "iterations", ["id"], unique=False)



def downgrade() -> None:
    op.drop_table("iterations")
    op.drop_table("conversations")

