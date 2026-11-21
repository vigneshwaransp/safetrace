from datetime import datetime, timezone
from typing import Dict, Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Application health status")
    version: str = Field(default="0.1.0", description="API version")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    environment: str = Field(default="development")
    services: Dict[str, Any] = Field(default_factory=dict)
