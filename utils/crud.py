from sqlmodel import Session, select
from db.models import User
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
