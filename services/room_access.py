from config import get_settings
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse

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


def make_room_access_token_response(room_id: int, username: str, url: str):
    token = create_room_access_token(room_id, username)
    response = RedirectResponse(url=url, status_code=302)
    response.set_cookie(
        key=f"room_{room_id}_access",
        value=token,
        httponly=True,
        max_age=60 * 30,
        samesite="lax",
    )
    return response
