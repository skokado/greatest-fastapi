from enum import StrEnum
import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnv(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


class Settings(BaseSettings):
    DEBUG: bool = False

    title: str = "My App"

    ENV: AppEnv = AppEnv(os.getenv("ENV", "local"))
    LOG_LEVEL: str = "INFO"

    DATABASE_HOST: str = ""
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = ""
    DATABASE_USER: str = ""
    DATABASE_PASSWORD: str = ""

    model_config = SettingsConfigDict(env_file=Path(__file__) / f"{ENV}.env")
