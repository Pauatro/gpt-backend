from pydantic import BaseModel
from shared.schemas import EntityBase


class UserBase(BaseModel):
    username: str


class User(UserBase, EntityBase):
    hashed_password: str


class CreateUser(UserBase):
    hashed_password: str


class PostUser(UserBase):
    password: str


class TokenPayload(BaseModel):
    sub: str  # username
    exp: int  # expiration time
