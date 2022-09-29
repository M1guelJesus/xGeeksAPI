from datetime import datetime
from typing import Any, Dict

import jwt
from fastapi import HTTPException
from pydantic import UUID4

from core.environment import config

KEY = config.get("jwt.secret")
TIME_LIMIT = 36000  # 1 day
ALGORITHM = "HS256"
ISSUER = "local"


def encode_password_token(user_id: UUID4) -> str:
    today = datetime.now().timestamp()
    return str(
        jwt.encode(
            payload={
                "exp": today + TIME_LIMIT,
                "iat": today,
                "user": str(user_id),
            },
            key=KEY,
            algorithm=ALGORITHM,
        ),
    )


def decode_password_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(
            key=KEY,
            jwt=token,
            algorithms=[
                ALGORITHM,
            ],
            options={"require": ["exp"]},
        )
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")
