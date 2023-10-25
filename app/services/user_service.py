from uvicorn.main import logger

from app.schema.requests.user_schema import CurrentUserRequest
from app.db.dao.user_dao import UserDao
from app.services.token_service import TokenService
from app.services.password_service import PasswordService
from app.exceptions import AppException
from datetime import datetime
from fastapi import status


class UserService:
    def __init__(self, db_pool=None):
        self.user_dao = UserDao()
        self.db_pool = db_pool

    async def get_current_user(self, request: CurrentUserRequest):
        payload = TokenService().decode(request.token)
        if payload.get("exp") is not None and datetime.utcnow().timestamp() > payload.get("exp"):
            raise AppException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )

        user_id = payload.get("sub")
        user_details = await self.user_dao.get_user({"id": user_id})

        if not user_details:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Username or Password")

        return user_details

    async def create_user(self, req):
        user_details = await self.user_dao.insert_dict({
            "username": req.username,
            "password": req.password,
            "email": req.email,
            "name": req.name,
            "phone_number": req.phone_number
        })
        return user_details

    async def get_token(self, request):
        user_details = await self.get_user_details_by_username(request.username)
        logger.info(f"user_details - {user_details}")
        if user_details and PasswordService.check_password(request.password, user_details.password):
            user_id = user_details.id
            token_service = TokenService()
            token = await token_service.get_access_token(request, user_id, self.db_pool)
            return token
        return None

    async def get_user_details_by_username(self, username: str):
        user_details = await self.user_dao.get_user({"username": username})
        logger.info(f"user_details - {user_details}")
        if user_details:
            return user_details[0]
        return None