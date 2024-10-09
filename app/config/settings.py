from enum import StrEnum
import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnv(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    STG = "stg"
    PRD = "prd"

ENV: AppEnv = AppEnv(os.getenv("ENV", "local"))

class Settings(BaseSettings):
    # --- for FastAPI() settings
    title: str = "My Greatest FastAPI"
    docs_url: Optional[str] = None if ENV == AppEnv.PRD else "/docs"
    DEBUG: bool = False
    LOG_LEVEL: str = "DEBUG" if ENV in (AppEnv.LOCAL, AppEnv.DEV) else "INFO"
    # --- end of FastAPI() settings

    DATABASE_HOST: str = ""
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = ""
    DATABASE_USER: str = ""
    DATABASE_PASSWORD: str = ""

    # Settings の値を {Env}.env によって上書きする
    model_config = SettingsConfigDict( env_file=Path(__file__).parent / f"{ENV}.env")
