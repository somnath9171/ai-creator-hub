import os
from datetime import datetime, timezone, timedelta
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "991823aBcDeFgHiJkLmNoPqRsTuVwXyZ_SUPER_SECURE_TOKEN_2026")
ALGORITHM = "HS256"
security_bearer = HTTPBearer()

class JWTManager:
    @classmethod
    def create_access_token(cls, telegram_id: int, role: str) -> str:
        payload = {
            "sub": str(telegram_id),
            "role": role,
            "exp": datetime.now(timezone.utc) + timedelta(days=7)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    def verify_token(cls, credentials: HTTPAuthorizationCredentials = Security(security_bearer)) -> dict:
        token = credentials.credentials
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Session token expired or signature validation failed.")
