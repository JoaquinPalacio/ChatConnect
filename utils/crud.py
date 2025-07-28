from fastapi import Request
from sqlmodel import Session, select
from sqlalchemy import desc, cast, DateTime
from db.models.room import Room
from db.models.user import User
from db.models.message import Message
from utils.security import hash_password, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from typing import Optional


def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def get_username_from_cookies(cookies: dict) -> str:
    token = cookies.get("access_token")
    if not token:
        return "Anon"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub", "Anon")
    except JWTError:
        return "Anon"


def get_username_from_request(request: Request) -> Optional[str]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


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


def verify_room_access_token(token: str, expected_room_id: int, username: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return (
            payload.get("room_id") == expected_room_id
            and payload.get("sub") == username
        )
    except JWTError:
        return False
