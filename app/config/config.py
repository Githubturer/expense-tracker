from pydantic_settings import BaseSettings
from pydantic import Field
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class Settings(BaseSettings):
    # Database
    database_url: str = Field(..., alias="DATABASE_URL")
    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., alias="POSTGRES_DB")
    
    # JWT
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # App
    environment: Environment = Field(..., alias="ENVIRONMENT")
    app_name: str = Field(..., alias="APP_NAME")
    debug: bool = Field(..., alias="DEBUG")

    #Logging
    log_level: str = Field(..., alias="LOG_LEVEL")
    sql_echo: bool = Field(..., alias="SQL_ECHO")

    def configure_logging_environment(self) -> None:
        if self.environment == Environment.PRODUCTION:
            self.log_level = "WARNING"
            self.sql_echo = False

    
    class Config:
        env_file = ".env"


settings = Settings()
settings.configure_logging_environment()