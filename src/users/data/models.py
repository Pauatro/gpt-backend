from shared.database import Base, get_uuid_column, get_timestamp_column
from sqlalchemy import Column, String, TIMESTAMP, text


class UserModel(Base):
    __tablename__ = "users"
    id = get_uuid_column()
    created_at = get_timestamp_column()
    updated_at = get_timestamp_column()

    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
