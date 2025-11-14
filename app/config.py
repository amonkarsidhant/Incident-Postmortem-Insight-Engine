from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/postmortems",
        description="Database connection URL.",
    )
    storage_dir: str = Field(default="storage", description="Directory for uploaded files.")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
