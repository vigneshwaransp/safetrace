import uuid
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field, HttpUrl
from app.schemas.match import MatchResponse


class DiscoveryJobCreate(BaseModel):
    platforms: Optional[List[str]] = Field(
        None,
        description="Target platforms (META, X, REDDIT, YOUTUBE, BLUESKY). Defaults to all."
    )


class DiscoveryJobResponse(BaseModel):
    id: uuid.UUID
    case_id: uuid.UUID
    status: str
    platforms_searched: List[str]
    results_count: int
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class DiscoveryJobDetailResponse(DiscoveryJobResponse):
    matches: List[MatchResponse] = []


class ManualUrlSubmission(BaseModel):
    url: str = Field(..., description="Direct public URL to inspect and compare")
