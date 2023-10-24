import json

from fastapi import APIRouter, Depends, Response, status
from psycopg_pool import AsyncConnectionPool

from app.db.connection import get_db_pool
from app.schema.requests.user_schema import CurrentUserRequest, CreateUserRequest, ResetPasswordRequest
from app.services.user_service import UserService

user_router = APIRouter()


@user_router.get("/me/{test}")
async def get_current_user(req: CurrentUserRequest = Depends(), db_pool: AsyncConnectionPool = Depends(get_db_pool)):
    service = UserService(db_pool)
    response = await service.get_current_user(req)
    return response

@user_router.post("/create")
async def create_user(req: CreateUserRequest = Depends(), db_pool: AsyncConnectionPool = Depends(get_db_pool)):
    service = UserService(db_pool)
    await service.create_user(req)
    return Response(
        status_code=status.HTTP_201_CREATED,
        content=json.dumps({"message": "User created"})
    )

@user_router.post("/reset-password")
def reset_password(req : ResetPasswordRequest = Depends()):
    return "200"