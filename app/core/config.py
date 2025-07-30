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
    access_secret_key: str = Field(..., alias="ACCESS_SECRET_KEY")
    refresh_secret_key: str = Field(..., alias="REFRESH_SECRET_KEY")
    password_reset_secret_key: str = Field(..., alias="PASSWORD_RESET_SECRET_KEY")
    verification_secret_key: str = Field(..., alias="VERIFICATION_SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(..., alias="REFRESH_TOKEN_EXPIRE_DAYS")
    verification_token_expire_minutes: int = Field(..., alias="VERIFICATION_TOKEN_EXPIRE_MINUTES")
    password_reset_token_expire_minutes: int = Field(..., alias="PASSWORD_RESET_TOKEN_EXPIRE_MINUTES")

    # App
    environment: Environment = Field(..., alias="ENVIRONMENT")
    app_name: str = Field(..., alias="APP_NAME")
    debug: bool = Field(..., alias="DEBUG")

    #Logging
    log_level: str = Field(..., alias="LOG_LEVEL")
    sql_echo: bool = Field(..., alias="SQL_ECHO")

    # Mailhog
    mail_server: str = Field(..., alias="MAIL_SERVER")
    mail_port: int = Field(..., alias="MAIL_PORT")
    mail_username: str = Field(..., alias="MAIL_USERNAME")
    mail_password: str = Field(..., alias="MAIL_PASSWORD")
    mail_from: str = Field(..., alias="MAIL_FROM")
    mail_use_tls: bool = Field(..., alias="MAIL_USE_TLS")
    mail_use_ssl: bool = Field(..., alias="MAIL_USE_SSL")

    def configure_logging_environment(self) -> None:
        if self.environment == Environment.PRODUCTION:
            self.log_level = "WARNING"
            self.sql_echo = False

    
    class Config:
        env_file = ".env"


settings = Settings()
settings.configure_logging_environment()