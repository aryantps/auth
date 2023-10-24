from fastapi import APIRouter, Depends, status
from psycopg_pool import AsyncConnectionPool

from app.db.connection import get_db_pool
from app.exceptions import AppException
from app.schema.requests.token_schema import TokenRequest
from app.services.user_service import UserService

token_router = APIRouter()


@token_router.post("/token")
async def get_token(req: TokenRequest = Depends()):
    user_service = UserService()
    token = await user_service.get_token(req)
    if token:
        return {"access_token": token}

    raise AppException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid Username or Password !"
    )