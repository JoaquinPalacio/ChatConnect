from sqlmodel import Session, select
from models.room import Room
from sqlalchemy import func
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


async def search_rooms(session: Session, q: str | None):
    statement = select(Room)
    if q:
        statement = statement.where(func.lower(Room.name).contains(q.lower()))
    return session.exec(statement).all()


def get_room_by_id(session: Session, room_id: int) -> Room | None:
    return session.get(Room, room_id)


def get_room_id_by_name(session: Session, room_name: str) -> int | None:
    room = session.exec(select(Room).where(Room.name == room_name)).first()
    return room.id if room else None
