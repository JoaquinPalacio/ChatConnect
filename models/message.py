from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int | None = Field(foreign_key="user.id")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    room_id: int | None = Field(foreign_key="room.id")
