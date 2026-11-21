import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.case import Case
from app.models.match import Match
from app.models.evidence import EvidenceItem
from app.schemas.match import MatchResponse, MatchReviewUpdate
from app.schemas.evidence import (
    EvidenceItemResponse,
    EvidenceVaultResponse,
    EvidenceExportResponse,
)
from app.services.evidence import (
    create_evidence_from_confirmed_match,
    verify_evidence_chain,
)
from app.api.deps import get_current_user, record_audit

router = APIRouter()


@router.patch("/matches/{match_id}", response_model=MatchResponse)
def review_match(
    match_id: uuid.UUID,
    review_in: MatchReviewUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Human-in-the-Loop Match Review:
    - Sets review status to CONFIRMED, REJECTED, or UNSURE
    - When CONFIRMED: automatically captures and cryptographically secures evidence in the tamper-evident hash chain
    - Mitigates false positives before reporting
    """
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    case = db.query(Case).filter(Case.id == match.case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Associated case not found")

    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized to review matches on this case")

    normalized_status = review_in.review_status.upper()
    if normalized_status not in ["CONFIRMED", "REJECTED", "UNSURE"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid review_status. Must be CONFIRMED, REJECTED, or UNSURE."
        )

    match.review_status = normalized_status
    match.reviewer_notes = review_in.reviewer_notes
    match.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(match)

    evidence_created = False
    if normalized_status == "CONFIRMED":
        evidence_item = create_evidence_from_confirmed_match(db=db, match=match)
        evidence_created = True

    record_audit(
        db=db,
        action=f"MATCH_{normalized_status}",
        user_id=current_user.id,
        case_id=case.id,
        details={
            "match_id": str(match.id),
            "platform": match.platform,
            "evidence_created": evidence_created
        },
        request=request
    )

    return match


@router.get("/cases/{case_id}/evidence", response_model=EvidenceVaultResponse)
def get_case_evidence_vault(
    case_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all confirmed evidence records in the tamper-evident vault:
    - Runs cryptographic verification on the append-only hash chain
    - Surfaces chain integrity status
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    items = (
        db.query(EvidenceItem)
        .filter(EvidenceItem.case_id == case_id)
        .order_by(EvidenceItem.created_at.asc())
        .all()
    )

    is_valid, reason = verify_evidence_chain(items)

    return EvidenceVaultResponse(
        case_id=case_id,
        total_items=len(items),
        is_chain_valid=is_valid,
        verification_message="Tamper-evident cryptographic hash chain is verified and intact." if is_valid else f"Integrity warning: {reason}",
        items=[EvidenceItemResponse.model_validate(it) for it in items],
    )


@router.get("/cases/{case_id}/evidence/{evidence_id}", response_model=EvidenceItemResponse)
def get_evidence_item(
    case_id: uuid.UUID,
    evidence_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve details for a single verified evidence record."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    item = db.query(EvidenceItem).filter(EvidenceItem.id == evidence_id, EvidenceItem.case_id == case_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Evidence item not found")

    return item


@router.post("/cases/{case_id}/evidence/export", response_model=EvidenceExportResponse)
def export_evidence_log(
    case_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export the tamper-evident cryptographic evidence bundle for legal or cybercrime complaints:
    - Includes SHA-256 chain signatures, capture UTC timestamps, and source URLs
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    items = (
        db.query(EvidenceItem)
        .filter(EvidenceItem.case_id == case_id)
        .order_by(EvidenceItem.created_at.asc())
        .all()
    )

    is_valid, _ = verify_evidence_chain(items)

    evidence_log = []
    for it in items:
        evidence_log.append({
            "evidence_number": it.evidence_number,
            "platform": it.platform,
            "source_url": it.source_url,
            "captured_at_utc": it.captured_at.isoformat(),
            "content_sha256": it.content_sha256,
            "similarity_score": it.similarity_score,
            "previous_evidence_hash": it.previous_evidence_hash,
            "evidence_hash": it.evidence_hash,
            "metadata_snapshot": it.metadata_snapshot,
        })

    record_audit(
        db=db,
        action="EVIDENCE_LOG_EXPORTED",
        user_id=current_user.id,
        case_id=case.id,
        details={"items_count": len(items), "chain_verified": is_valid},
        request=request
    )

    return EvidenceExportResponse(
        export_id=uuid.uuid4(),
        export_timestamp=datetime.now(timezone.utc),
        case_id=case_id,
        total_evidence_items=len(items),
        chain_verified=is_valid,
        evidence_log=evidence_log,
    )
