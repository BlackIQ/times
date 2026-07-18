# Datetime
from datetime import datetime, timedelta, timezone

# JWT
import jwt

# Application
from core.settings import settings  # Settings

# Secret and Algo
SECRET = settings.secret
ALGORITHM = settings.algorithm


def create_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=7)

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    jwt_token = jwt.encode(payload=payload, key=SECRET, algorithm=ALGORITHM)

    return jwt_token
