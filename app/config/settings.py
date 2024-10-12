from enum import StrEnum
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppEnv(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    STG = "stg"
    PRD = "prd"

ENV: AppEnv = AppEnv(os.getenv("ENV", "local"))

dotenv_path = Path(__file__).parent / f"{ENV}.env"
if dotenv_path.exists():
    load_dotenv(dotenv_path, override=False)


class Settings(BaseSettings):
    # --- for FastAPI() settings
    title: str = "My Greatest FastAPI"
    docs_url: Optional[str] = None if ENV == AppEnv.PRD else "/docs"
    DEBUG: bool = False
    LOG_LEVEL: str = "DEBUG" if ENV in (AppEnv.LOCAL, AppEnv.DEV) else "INFO"

    SECRET_KEY: str = os.environ["SECRET_KEY"]
    # --- end of FastAPI() settings

    DATABASE_HOST: str = os.environ["DATABASE_HOST"]
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", 5432))
    DATABASE_NAME: str = os.environ["DATABASE_NAME"]
    DATABASE_USER: str = os.environ["DATABASE_USER"]
    DATABASE_PASSWORD: str = os.environ["DATABASE_PASSWORD"]

    DATABASE_URL: str = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    # Settings の値を {Env}.env によって上書きする
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / f"{ENV}.env")
