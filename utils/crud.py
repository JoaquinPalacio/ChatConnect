from sqlmodel import Session, select
from db.models import User, Message
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


def get_last_messages(session: Session, limit: int = 30):
    statement = (
        select(Message, User.username)
        .join(User, Message.user_id == User.id, isouter=True)
        .order_by(Message.timestamp.desc())
        .limit(limit)
    )
    results = session.exec(statement).all()
    return [
        {
            "username": username or "Anon",
            "content": msg.content,
            "timestamp": msg.timestamp,
        }
        for msg, username in reversed(results)
    ]
