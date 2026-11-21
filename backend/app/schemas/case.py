import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.image import CaseImageResponse


class CaseCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, description="Case title")
    description: Optional[str] = Field(None, description="Confidential incident summary")
    is_pseudonymous: bool = Field(default=False, description="Whether to mask user identity in reports")
    pseudonym: Optional[str] = Field(None, description="Optional chosen alias")
    retain_encrypted_originals: bool = Field(
        default=False,
        description="Whether to retain AES-encrypted original media. Default is false (hash-only privacy)."
    )


class CaseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    pseudonym: Optional[str] = None
    status: Optional[str] = Field(None, description="ACTIVE, CLOSED, or ARCHIVED")
    retain_encrypted_originals: Optional[bool] = None


class CaseResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    description: Optional[str] = None
    is_pseudonymous: bool
    pseudonym: Optional[str] = None
    status: str
    retain_encrypted_originals: bool
    created_at: datetime
    updated_at: datetime
    image_count: int = 0
    matches_count: int = 0

    model_config = {"from_attributes": True}


class CaseDetailResponse(CaseResponse):
    images: List[CaseImageResponse] = []
