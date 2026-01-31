from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from jwt import PyJWTError

from apps.user.models import User
from config.settings import (
    JWT_ACCESS_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
)


def generate_jwt_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_EXPIRE_MINUTES)
    payload = {
        "sub": str(user.username),
        "exp": expire,
    }
    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def verify_jwt_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
        return payload.get("sub")
    except PyJWTError:
        return None
