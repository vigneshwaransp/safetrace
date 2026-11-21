import json
from pathlib import Path
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SafeTrace"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security & Cryptography
    SECRET_KEY: str = "safetrace-insecure-secret-key-change-in-production-min-32-chars-long"
    # AES-256 Fernet key (32 bytes base64 encoded)
    ENCRYPTION_KEY: str = "MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTIzNDU2Nzg5MDE="
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # Database
    # Default to SQLite for easy local dev/test if postgres not present; overridden in docker/env
    DATABASE_URL: str = "sqlite:///./safetrace.db"
    
    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # File Storage
    STORAGE_DIR: str = "storage"
    UPLOAD_MAX_BYTES: int = 26214400 # 25 MB
    
    # CORS
    BACKEND_CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, str) and v.startswith("["):
            try:
                return json.loads(v)
            except Exception:
                return [v]
        return v

    # Matching Thresholds (Hamming Distance for PDQ & Perceptual Hashes)
    PDQ_THRESHOLD_HIGH: int = 20      # Hamming distance <= 20 is high confidence
    PDQ_THRESHOLD_MEDIUM: int = 31    # Hamming distance <= 31 is medium candidate
    PHASH_THRESHOLD_HIGH: int = 10
    PHASH_THRESHOLD_MEDIUM: int = 18

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def storage_path(self) -> Path:
        p = Path(self.STORAGE_DIR)
        p.mkdir(parents=True, exist_ok=True)
        return p


settings = Settings()
