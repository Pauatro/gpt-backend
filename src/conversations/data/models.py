from shared.database import Base, get_uuid_column, get_timestamp_column
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
)


class ConversationModel(Base):
    __tablename__ = "conversations"
    id = get_uuid_column()
    created_at = get_timestamp_column()
    updated_at = get_timestamp_column()

    user_id = mapped_column(ForeignKey("users.id"))
    title = Column(String, nullable=False)
    iterations: Mapped[List["IterationModel"]] = relationship()


class IterationModel(Base):
    __tablename__ = "iterations"
    id = get_uuid_column()
    created_at = get_timestamp_column()
    updated_at = get_timestamp_column()

    conversation_id = mapped_column(ForeignKey("conversations.id"))
    request = Column(String, nullable=False)
    response = Column(String, nullable=False)
