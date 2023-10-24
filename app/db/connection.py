import psycopg_pool
from psycopg_pool import AsyncConnectionPool
from fastapi import FastAPI
from app.config.settings import settings
from starlette.requests import Request
from uvicorn.main import logger


async def setup_db(app: FastAPI) -> None:
    """
    Creates connection pool

    :param app: current FastAPI app.
    """
    logger.info("DB set up Intialized.......")
    app.state.db_pool = psycopg_pool.AsyncConnectionPool(conninfo=str(settings.get_db_url))
    await app.state.db_pool.wait()

async def check_db_connection(app: FastAPI) -> None:
    if not hasattr(app.state, "db_pool") or app.state.db_pool is None:
        logger.error("DB connection pool is not set up!")
        return

    connection = await app.state.db_pool.getconn()
    try:
        cursor = connection.cursor()
        await cursor.execute("SELECT 1;")
        result = await cursor.fetchone()
        logger.info("DB connection is working: %s", result)
    finally:
        await app.state.db_pool.putconn(connection)


async def get_db_pool(request: Request) -> AsyncConnectionPool:
    """
    Return database connections pool.

    :param request: current request.
    :returns: database connections pool.
    """
    return request.app.state.db_pool
