import os
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Event Ticketing API"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False

    # Database
    database_uri: str = os.getenv(
        "DATABASE_URI",
        "postgresql+asyncpg://admin:admin_pass@localhost:5432/ticketing_db",
    )
    database_echo: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
