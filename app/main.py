import uvicorn
from uvicorn.main import logger
from app.config.settings import settings
from app.resources.api import app

if __name__ == "__main__":
    logger.info("Starting server........")
    print(settings.get_db_url)

    uvicorn.run(
        app,
        workers=settings.WORKERS_COUNT,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LVL.value.lower(),
    )