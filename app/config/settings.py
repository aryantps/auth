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

    TOKEN_PRIVATE_KEY: str  
    TOKEN_PUBLIC_KEY: str  

    # Variables for the database
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Load private key and public key from files
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_keys_from_files()

    def load_keys_from_files(self):
        # Load the contents of private key from private_key.pem
        with open('private_key.pem', 'r') as private_key_file:
            self.TOKEN_PRIVATE_KEY = private_key_file.read()

        # Load the contents of public key from public_key.pem
        with open('public_key.pem', 'r') as public_key_file:
            self.TOKEN_PUBLIC_KEY = public_key_file.read()

    @property
    def get_db_url(self) -> URL:
        """
        get db URL.

        :return: database URL.
        """
        return URL.build(
            scheme="postgres",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=f"/{self.POSTGRES_DB}",
        )

    @property
    def get_postgres_conn_string(self):
        """
        Get the database URL with SSL mode disabled.
        """
        return f"postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}?sslmode=disable"

    @property
    def get_asyncpg_conn_string(self):
        """
        Get the asyncpg URL.
        """
        return f"asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()