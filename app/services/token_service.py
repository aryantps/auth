from app.config.settings import settings
from app.db.dao.session_dao import SessionDao
import jwt
from uvicorn.main import logger
from datetime import datetime

class TokenService:

    async def get_access_token(self, request, user_id, db_pool):
        payload = {
            "sub": user_id,
            "iss": "AuthApp",
            "aud": "users",
            "exp": request.expiration_time,
            "iat": request.issued_time,
        }
        token = self.encode(payload)
        session_dao = SessionDao()
        await session_dao.insert_dict({
            "token": token,
            "created_at": datetime.utcnow(),
            "expiring_at": datetime.now(),
            "user_id": user_id
        })
        return token

    def encode(self, payload: dict) -> str:
        return jwt.encode(payload, settings.TOKEN_PRIVATE_KEY, algorithm="RS256")

    def decode(self, encoded: str) -> dict:
        try:
            return jwt.decode(encoded, settings.TOKEN_PUBLIC_KEY, algorithms=["RS256"], options={"verify_aud": False})
        except (jwt.InvalidSignatureError, jwt.ExpiredSignatureError):
            return {}

