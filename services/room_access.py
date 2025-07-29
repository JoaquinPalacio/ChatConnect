from config import get_settings
from jose import jwt, JWTError
from datetime import datetime, timedelta

settings = get_settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.jwt_algorithm


def create_room_access_token(
    room_id: int, username: str, expires_minutes: int = 30
) -> str:
    to_encode = {
        "room_id": room_id,
        "sub": username,
        "exp": datetime.now() + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_room_access_token(token: str, expected_room_id: int, username: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return (
            payload.get("room_id") == expected_room_id
            and payload.get("sub") == username
        )
    except JWTError:
        return False
