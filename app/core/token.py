from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import jwt
from app.config import settings


async def create_jwt_token(username: str) -> str:
    utcnow = datetime.now(tz=timezone.utc)
    token_expire = utcnow + timedelta(minutes=settings.token_expire_minutes)
    payload = {
        "username": username,
        "exp": token_expire.timestamp(),
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        settings.jwt_algorithm,
    )


async def decode_jwt_token(token: str) -> Optional[dict[str, Any]]:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            [settings.jwt_algorithm],
        )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
