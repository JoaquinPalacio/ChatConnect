from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from config import get_settings

settings = get_settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.jwt_algorithm


def create_acces_token(data: dict, expires_delta: Optional[timedelta]):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
