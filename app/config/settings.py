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


override_env_path = Path(__file__).parent.parent / ".env.override"
if override_env_path.exists():
    load_dotenv(override_env_path, override=True)


class Settings(BaseSettings):
    # --- for FastAPI() settings
    title: str = "My Greatest FastAPI"
    docs_url: Optional[str] = None if ENV == AppEnv.PRD else "/docs"
    DEBUG: bool = False
    LOG_LEVEL: str = "DEBUG" if ENV in (AppEnv.LOCAL, AppEnv.DEV) else "INFO"

    # --- Secrets
    SECRET_KEY: str = ""
    HASH_ALGORITHM: str = "HS512"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

    # --- Database
    DATABASE_HOST: str = os.environ["DATABASE_HOST"]
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", 5432))
    DATABASE_NAME: str = os.environ["DATABASE_NAME"]
    DATABASE_USER: str = os.environ["DATABASE_USER"]
    DATABASE_PASSWORD: str = os.environ["DATABASE_PASSWORD"]

    DATABASE_URL: str = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    # --- Auth0
    AUTH0_DOMAIN: str = os.getenv("AUTH0_DOMAIN", "")
    AUTH0_CLIENT_ID: str = os.getenv("AUTH0_CLIENT_ID", "")
    AUTH0_CLIENT_SECRET: str = os.getenv("AUTH0_CLIENT_SECRET", "")
    AUTH0_ALGORITHMS: list[str] = ["RS256"]
    AUTH0_CALLBACK_URL: str = ""
    AUTH0_AUDIENCE: str = os.getenv("AUTH0_AUDIENCE", "")
    AUTH0_JWKS_URI: str = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"

    # Settings の値を {Env}.env によって上書きする
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / f"{ENV}.env")
