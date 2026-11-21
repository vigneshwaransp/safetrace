import uuid
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    report_type: str = Field(
        ...,
        description="PLATFORM_TAKEDOWN, CYBERCRIME_GOV, POLICE_COMPLAINT, or NGO_SUBMISSION"
    )
    title: str = Field(..., min_length=5, max_length=255)
    selected_evidence_ids: List[uuid.UUID] = Field(..., min_length=1, description="List of confirmed evidence IDs to bundle")
    recipient_platform: Optional[str] = Field(None, description="Platform targeted if PLATFORM_TAKEDOWN")
    custom_notes: Optional[str] = Field(None, description="Additional victim statement or background")


class ReportStatusUpdate(BaseModel):
    status: str = Field(..., description="DRAFT, SUBMITTED, ACKNOWLEDGED, REMOVED, REJECTED, REAPPEARED")
    notes: Optional[str] = Field(None, description="Status update commentary or platform response code")


class ReportStatusHistoryResponse(BaseModel):
    id: uuid.UUID
    report_id: uuid.UUID
    previous_status: str
    new_status: str
    notes: Optional[str] = None
    changed_by_user_id: Optional[uuid.UUID] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ReportResponse(BaseModel):
    id: uuid.UUID
    case_id: uuid.UUID
    report_number: str
    report_type: str
    title: str
    recipient_platform: Optional[str] = None
    selected_evidence_ids: List[str]
    report_content: Optional[str] = None
    pdf_available: bool = False
    status: str
    created_at: datetime
    updated_at: datetime
    status_history: List[ReportStatusHistoryResponse] = []

    model_config = {"from_attributes": True}
