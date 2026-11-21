import uuid
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field


class MatchResponse(BaseModel):
    id: uuid.UUID
    case_id: uuid.UUID
    discovery_job_id: Optional[uuid.UUID] = None
    case_image_id: uuid.UUID
    platform: str
    source_url: str
    author_handle: Optional[str] = None
    post_timestamp: Optional[datetime] = None
    thumbnail_url: Optional[str] = None
    media_url: Optional[str] = None
    sha256_hash: Optional[str] = None
    similarity_score: float
    confidence_band: str
    match_reasons: List[str]
    review_status: str
    reviewed_at: Optional[datetime] = None
    reviewer_notes: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class MatchReviewUpdate(BaseModel):
    review_status: str = Field(..., description="CONFIRMED, REJECTED, or UNSURE")
    reviewer_notes: Optional[str] = Field(None, description="Optional notes on verification rationale")
