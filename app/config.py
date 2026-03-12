from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    app_name: str = "VidyaMitra API"
    app_env: str = "development"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 120
    algorithm: str = "HS256"
    database_url: str = "sqlite:///./vidyamitra.db"
    upload_dir: str = "backend/storage/uploads"
    max_upload_size_mb: int = 5
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def absolute_upload_dir(self) -> Path:
        return BASE_DIR.parent / self.upload_dir


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.absolute_upload_dir.mkdir(parents=True, exist_ok=True)
    return settings
