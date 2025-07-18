from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int | None = Field(foreign_key="user.id")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    room_id: int | None = Field(foreign_key="room.id")


class Room(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    owner_id: int | None = Field(foreign_key="user.id")
    is_private: bool = Field(default=False)
    hashed_password: Optional[str] = None
