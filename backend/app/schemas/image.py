import uuid
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel


class CaseImageResponse(BaseModel):
    id: uuid.UUID
    case_id: uuid.UUID
    original_filename: str
    file_size: int
    mime_type: str
    sha256_hash: str
    pdq_hash: Optional[str] = None
    pdq_quality: Optional[int] = None
    phash: Optional[str] = None
    dhash: Optional[str] = None
    ahash: Optional[str] = None
    keypoints_summary: Optional[Any] = None
    is_encrypted: bool
    is_original_deleted: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ImagePurgeResponse(BaseModel):
    image_id: uuid.UUID
    message: str
    is_original_deleted: bool
    sha256_retained: str
