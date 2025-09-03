from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",  # permit unrelated env vars like GEMINI_API_KEY
    )

    app_name: str = "project_hermes"
    environment: str = "dev"  # dev | staging | prod
    log_level: str = "INFO"

    # Server
    host: str = "0.0.0.0"
    port: int = 8001
    cors_origins: str = "*"  # comma-separated

    # Providers / Backends (placeholders)
    redis_url: str = "redis://redis:6379/0"
    broker_url: str = "redis://redis:6379/1"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


