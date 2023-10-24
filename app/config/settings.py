import enum
from dotenv import load_dotenv
from pydantic import BaseSettings
from yarl import URL

load_dotenv()

class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"

class Settings(BaseSettings):
    HOST:str
    PORT:int
    WORKERS_COUNT: int = 1
    RELOAD: bool = False
    LOG_LVL: LogLevel = LogLevel.INFO

    TOKEN_PRIVATE_KEY : str
    TOKEN_PUBLIC_KEY: str

    # Variables for the database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "aryant"
    DB_PASS: str = "aryant"
    DB_BASE: str = "auth"
    DB_ECHO: bool = False

    # @property
    # def get_db_url(self) -> URL:
    #     """
    #     get db URL.
    #
    #     :return: database URL.
    #     """
    #     return URL.build(
    #         scheme="postgresql",
    #         host=self.DB_HOST,
    #         port=self.DB_PORT,
    #         user=self.DB_USER,
    #         password=self.DB_PASS,
    #         path=f"/{self.DB_BASE}",
    #         )
    @property
    def get_db_url(self) -> URL:
        """
        get db URL.

        :return: database URL.
        """
        return URL.build(
            scheme="postgres",
            host=self.DB_HOST,
            port=self.DB_PORT,
            user=self.DB_USER,
            password=self.DB_PASS,
            path=f"/{self.DB_BASE}",
        )


settings = Settings()