# from psycopg_pool import AsyncConnectionPool
# from fastapi import Depends
# from app.db.connection import get_db_pool
# from app.db.dao import BaseDao
# from typing import Dict
#
#
# class SessionDao(BaseDao):
#     def __init__(self, db_pool: AsyncConnectionPool = Depends(get_db_pool)):
#         super().__init__("sessions", db_pool)
#
#     async def insert_dict(self, session: Dict):
#         await super().insert(session)
#
#     async def get_session_details(self, filter_dict: Dict):
#         return await super().get(filter_dict)
#


from tortoise import Tortoise

from app.db.dao import BaseDao
from app.db.models.session_model import Session
from uvicorn.main import logger


class SessionDao(BaseDao):
    async def insert_dict(self, session):
        logger.info(f"get_access_token done - {session}")
        await self.insert(Session, session)

    async def get_session_details(self, filter_dict):
        return await self.get(Session, filter_dict)
