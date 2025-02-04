from functools import lru_cache
from logging.config import dictConfig
from pathlib import Path
from typing import Any, Dict, Union

from decouple import config
from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASEDIR = Path.cwd()

LOG_LEVEL = config("LOG_LEVEL", default="debug").upper()
LOG_DIR = BASEDIR / "logs"


dictConfig(
    dict(
        version=1,
        formatters={
            "default": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
            },
            "rich": {"datefmt": "[%X]"},
        },
        handlers={
            "console": {
                "class": "rich.logging.RichHandler",
                "formatter": "rich",
                "level": "DEBUG",
                "rich_tracebacks": True,
            },
            "file": {
                "level": "DEBUG",
                "formatter": "default",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": LOG_DIR / "app.log",
                "when": "D",
                "interval": 1,
                "backupCount": 7,
            },
        },
        root={"handlers": ["console"], "level": "DEBUG"},
        loggers={
            "app": {
                "level": LOG_LEVEL,
                "handlers": ["console", "file"],
                "propagate": False,
            }
        },
    )
)


class Config(BaseSettings):
    VERSION: str = Field(default="v1", json_schema_extra=dict(env="VERSION"))
    DEBUG: bool = Field(default=False, json_schema_extra=dict(env="DEBUG"))

    POSTGRES_USER: str = Field(default="", json_schema_extra=dict(env="POSTGRES_USER"))
    POSTGRES_PASSWORD: str = Field(
        default="", json_schema_extra=dict(env="POSTGRES_PASSWORD")
    )
    POSTGRES_HOST: str = Field(default="", json_schema_extra=dict(env="POSTGRES_HOST"))
    POSTGRES_PORT: str = Field(default="", json_schema_extra=dict(env="POSTGRES_PORT"))
    POSTGRES_DB: str = Field(default="", json_schema_extra=dict(env="POSTGRES_DB"))
    DATABASE_URL: Union[str, None] = None

    @field_validator("DATABASE_URL", mode="before")
    def build_db_connection(cls, v: Union[str, None], values: Dict[str, Any]) -> Any:
        if v:
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=values.data.get("POSTGRES_USER"),
                password=values.data.get("POSTGRES_PASSWORD"),
                host=values.data.get("POSTGRES_HOST"),
                port=int(values.data.get("POSTGRES_PORT")),
                path=f"{values.data.get('POSTGRES_DB') or ''}",
            )
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class TestingConfig(Config):
    @field_validator("DATABASE_URL")
    def build_db_connection(cls, v: Union[str, None]) -> Any:
        return "sqlite+aiosqlite://"


@lru_cache
def get_config():
    return Config()


@lru_cache
def get_testing_config():
    return TestingConfig()


CONFIG = get_config()
TESTING_CONFIG = get_testing_config()
