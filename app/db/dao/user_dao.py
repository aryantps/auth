# from psycopg_pool import AsyncConnectionPool
# from fastapi import Depends
# from app.db.connection import get_db_pool
# from app.db.dao import BaseDao
# from typing import Dict
#
#
# class UserDao(BaseDao):
#     def __init__(self, db_pool: AsyncConnectionPool = Depends(get_db_pool)):
#         super().__init__("users", db_pool)
#
#     async def insert_dict(self, user: Dict):
#         await super().insert(user)
#
#     async def get_user(self, filter_dict: Dict):
#         return await super().get(filter_dict)
#
from tortoise import Tortoise

from app.db.dao import BaseDao
from app.db.models.user_model import User


class UserDao(BaseDao):
    async def insert_dict(self, user):
        await self.insert(User, user)

    async def get_user(self, filter_dict):
        return await self.get(User, filter_dict)
