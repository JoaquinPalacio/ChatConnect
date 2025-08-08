from fastapi import Request, Depends, status, HTTPException
from sqlmodel import Session, select
from models.user import User
from core.security import hash_password, decode_access_token
from typing import Optional
from db.database import get_session


def create_user(session: Session, username: str, password: str):
    user = User(username=username, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def get_username_from_cookies(cookies: dict) -> str:
    token = str(cookies.get("access_token"))
    return decode_access_token(token) or "Anon"


def get_username_from_request(request: Request) -> Optional[str]:
    token = str(request.cookies.get("access_token"))
    return decode_access_token(token)


def get_user_from_request(session: Session, request: Request):
    username = get_username_from_request(request)
    if username is None:
        return None
    return get_user_by_username(session, str(username))


def get_current_user(request: Request, session: Session = Depends(get_session)):
    user = get_user_from_request(session, request)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
