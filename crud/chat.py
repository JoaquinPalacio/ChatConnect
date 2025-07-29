from sqlmodel import Session, select
from sqlalchemy import desc, cast, DateTime
from models.user import User
from models.message import Message


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


def get_last_30_messages(session: Session, limit: int = 30, room_id: int | None = None):
    statement = select(Message, User.username).outerjoin(User)
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
