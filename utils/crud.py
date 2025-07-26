from sqlmodel import Session, select
from sqlalchemy import desc, cast, DateTime
from db.models.room import Room
from db.models.user import User
from db.models.message import Message
from utils.security import hash_password


def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def create_user(session: Session, username: str, password: str):
    user = User(username=username, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_message(
    session: Session,
    content: str,
    user_id: int | None = None,
    room_id: int | None = None,
):
    message = Message(user_id=user_id, content=content, room_id=room_id)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def get_last_messages(session: Session, limit: int = 30, room_id: int | None = None):

    statement = (
        select(Message, User.username)
        .outerjoin(User)
    )
    if room_id is not None:
        statement = statement.where(Message.room_id == room_id)
    statement = statement.order_by(desc(cast(Message.timestamp, DateTime))).limit(limit)
    results = session.exec(statement).all()
    return [
        {
            "username": username or "Anon",
            "content": msg.content,
            "timestamp": msg.timestamp,
        }
        for msg, username in reversed(results)
    ]


def create_room(
        session: Session,
        name: str,
        owner_id: int | None = None,
        is_private: bool = False,
        password: str | None = None):
    room = Room(
        name=name,
        owner_id=owner_id,
        is_private=bool(is_private),
        hashed_password=hash_password(password) if password else None
    )
    session.add(room)
    session.commit()
    session.refresh(room)
    return room