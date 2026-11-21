import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class EvidenceItemResponse(BaseModel):
    id: uuid.UUID
    case_id: uuid.UUID
    match_id: uuid.UUID
    evidence_number: str
    platform: str
    source_url: str
    captured_at: datetime
    content_sha256: str
    screenshot_storage_path: Optional[str] = None
    similarity_score: float
    metadata_snapshot: Dict[str, Any]
    previous_evidence_hash: str
    evidence_hash: str
    created_at: datetime

    model_config = {"from_attributes": True}


class EvidenceVaultResponse(BaseModel):
    case_id: uuid.UUID
    total_items: int
    is_chain_valid: bool
    verification_message: str
    items: List[EvidenceItemResponse]


class EvidenceExportResponse(BaseModel):
    export_id: uuid.UUID
    export_timestamp: datetime
    case_id: uuid.UUID
    total_evidence_items: int
    chain_verified: bool
    evidence_log: List[Dict[str, Any]]
