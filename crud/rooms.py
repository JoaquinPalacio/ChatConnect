from sqlmodel import Session
from models.room import Room
from core.security import hash_password


def create_room(
    session: Session,
    name: str,
    owner_id: int | None = None,
    is_private: bool = False,
    password: str | None = None,
):
    room = Room(
        name=name,
        owner_id=owner_id,
        is_private=bool(is_private),
        hashed_password=hash_password(password) if password else None,
    )
    session.add(room)
    session.commit()
    session.refresh(room)
    return room
