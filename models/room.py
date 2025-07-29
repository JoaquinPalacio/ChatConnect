from sqlmodel import Field, SQLModel
from typing import Optional


class Room(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    owner_id: int | None = Field(foreign_key="user.id")
    is_private: bool = Field(default=False)
    hashed_password: Optional[str] = None
