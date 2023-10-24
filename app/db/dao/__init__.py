# from psycopg_pool import AsyncConnectionPool
# from fastapi import Depends
# from app.db.connection import get_db_pool
# from typing import Dict
# from psycopg.rows import dict_row
# from uvicorn.main import logger
# from psycopg.errors import UniqueViolation
#
#
# class BaseDao:
#     def __init__(self,
#                  table_name: str,
#                  db_pool: AsyncConnectionPool = Depends(get_db_pool)):
#         self.db_pool = db_pool
#         self.table_name = table_name
#
#     async def insert(self, data: Dict):
#         async with self.db_pool.connection() as connection:
#             async with connection.cursor(binary=True) as cur:
#                 columns = ", ".join(data.keys())
#                 values = ", ".join([f"%({key})s" for key in data.keys()])
#                 query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values});"
#                 logger.info(f"insert query - {query}")
#                 try:
#                     await cur.execute(query, params=data)
#                 except UniqueViolation as e:
#                     logger.error(str(e))
#                     raise e
#
#     async def get(self, filter_dict: Dict):
#         async with self.db_pool.connection() as connection:
#             async with connection.cursor(
#                     binary=True, row_factory=dict_row
#             ) as cur:
#                 columns = ", ".join(filter_dict.keys())
#                 placeholders = " AND ".join(
#                     [f"{key} = %({key})s" for key in filter_dict.keys()]
#                 )
#                 query = f"SELECT * FROM {self.table_name} WHERE {placeholders};"
#                 logger.info(f"get query - {query}")
#                 await cur.execute(query, params=filter_dict)
#                 return await cur.fetchall()
#
#     async def execute(self, query, data, response=True, connection=None):
#         connection = connection or self.db_pool.connection
#         cursor = connection.cursor(row_factory=dict_row)
#         try:
#             logger.info(f"Executing - {cursor.mogrify(query, data)}")
#             await cursor.execute(query, data)
#             if response:
#                 response = await cursor.fetchall()
#         except Exception as e:
#             raise e
#         finally:
#             if not connection and self.db_pool.connection:
#                 self.db_pool.connection.close()
#         return response



from tortoise import Tortoise
from tortoise.expressions import Q

class BaseDao:
    async def insert(self, model, data):
        await model.create(**data)

    async def get(self, model, filter_dict):
        query = Q(**filter_dict)
        return await model.filter(query)

    async def execute(self, query, data, response=True, connection=None):
        connection = connection or Tortoise.get_connection()
        try:
            result = await connection.execute_query(query, data)
            if response:
                return result
        except Exception as e:
            raise e
        finally:
            if not connection.closed:
                await connection.release()
