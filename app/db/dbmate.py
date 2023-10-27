import os
import subprocess
from uvicorn.main import logger
from app.config.settings import settings

def turn_dbmate_up():

    os.environ["DATABASE_URL"] = settings.get_postgres_conn_string
    os.environ["DBMATE_MIGRATIONS_DIR"] = "./app/db/migrations"

    logger.info("Turning up dbmate.......")

    p = subprocess.Popen("dbmate up",
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        logger.info(line)

def turn_dbmate_down():
    logger.info("Turning down dbmate.......")
    p = subprocess.Popen("dbmate down",
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        logger.info(line)

