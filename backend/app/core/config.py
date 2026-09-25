"""Application settings, loaded from environment variables / `.env`.

Nothing sensitive is ever hard-coded: every value can be overridden through
the environment (see `.env.example`).

Field names map to upper-case environment variables, e.g. `app_name` is read
from `APP_NAME`.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ----- Application -------------------------------------------------
    app_name: str = "crop-care-backend"
    app_version: str = "0.1.0"
    environment: Literal["local", "development", "staging", "production"] = "local"
    debug: bool = False
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"

    # ----- CORS ---------------------------------------------------------
    # Comma-separated list, e.g. "http://localhost:3000,https://app.example.com"
    # (kept as a string so it is friendly to write in .env files)
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        """`cors_origins` parsed into a list, ready for CORSMiddleware."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    # ----- Database (Database Integration task) --------------------------
    # Example: postgresql+asyncpg://user:password@localhost:5432/cropcare
    database_url: str = ""
    db_echo: bool = False

    # ----- ML (ML Integration task) --------------------------------------
    ml_model_dir: Path = Path("ml_models")
    disease_model_filename: str = "crop_disease_model.pt"
    ml_device: str = "cpu"
    max_upload_size_mb: int = Field(default=10, gt=0)

    @property
    def disease_model_path(self) -> Path:
        """Full path of the crop disease model artifact."""
        return self.ml_model_dir / self.disease_model_filename

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    # ----- LLM / chatbot (Chatbot Integration task) ----------------------
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings object (cached)."""
    return Settings()