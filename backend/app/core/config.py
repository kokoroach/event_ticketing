from typing import Annotated, Literal
from zoneinfo import ZoneInfo

from pydantic import AnyUrl, BeforeValidator, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: str | list) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


def parse_timezone(v: str | ZoneInfo) -> ZoneInfo:
    """Convert timezone string to a ZoneInfo object."""
    if isinstance(v, ZoneInfo):
        return v
    try:
        return ZoneInfo(v)
    except Exception as e:
        raise ValueError(f"Invalid timezone: {v}") from e


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    # Dev Environment
    ENVIRONMENT: Literal["local", "stage", "prod"] = "local"

    # Application
    PROJECT_NAME: str = "Full Stack Event Ticketing API"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Backend
    DEFAULT_TIMEZONE: Annotated[ZoneInfo, BeforeValidator(parse_timezone)] = "UTC"  # type: ignore[assignment]  # handled by beforeValidator
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[misc]
    @property
    def DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    DATABASE_ECHO: bool = False

    # Frontend
    FRONTEND_HOST: str = "http://localhost:5173"


settings = Settings()
