from functools import lru_cache
from logging.config import dictConfig
from pathlib import Path
from typing import Any

from decouple import config
from pydantic import Field, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path.cwd()

LOG_LEVEL = config("LOG_LEVEL", default="debug").upper()
LOG_DIR = BASE_DIR / "logs"
PROMPT_TEMPLATES_DIR = BASE_DIR / "app/common/prompt_templates"


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
    VERSION: str = Field(default="v1")
    DEBUG: bool = Field(default=False)

    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DB: str = Field(default="postgres")
    OLLAMA_DOMAIN: str = Field(default="localhost")
    OLLAMA_PORT: str = Field(default="11434")
    OLLAMA_GENERATION_MODEL: str
    OLLAMA_EMBEDDING_MODEL: str

    DATABASE_URL: str = Field(default="")
    PGAI_DATABASE_URL: str = Field(default="")
    OLLAMA_HOST: str = Field(default="")

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def build_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if v:
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=info.data.get("POSTGRES_USER"),
                password=info.data.get("POSTGRES_PASSWORD"),
                host=info.data.get("POSTGRES_HOST"),
                port=info.data.get("POSTGRES_PORT"),
                path=info.data.get("POSTGRES_DB"),
            )
        )
    
    @field_validator("PGAI_DATABASE_URL", mode="before")
    @classmethod
    def build_pgai_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if v:
            return v

        return str(
            PostgresDsn.build(
                scheme="postgres",
                username=info.data.get("POSTGRES_USER"),
                password=info.data.get("POSTGRES_PASSWORD"),
                host=info.data.get("POSTGRES_HOST"),
                port=info.data.get("POSTGRES_PORT"),
                path=info.data.get("POSTGRES_DB"),
            )
        )
    
    

    @field_validator("OLLAMA_HOST", mode="before")
    @classmethod
    def build_ollama_host(cls, v: str | None, info: ValidationInfo) -> Any:
        if v:
            return v

        return f"http://{info.data.get('OLLAMA_DOMAIN')}:{info.data.get('OLLAMA_PORT')}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_config():
    return Config()


CONFIG = get_config()
