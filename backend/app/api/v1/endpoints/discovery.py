import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.case import Case
from app.models.match import Match
from app.models.discovery_job import DiscoveryJob
from app.schemas.discovery import (
    DiscoveryJobCreate,
    DiscoveryJobResponse,
    ManualUrlSubmission,
)
from app.schemas.match import MatchResponse
from app.services.discovery import (
    run_discovery_for_case,
    process_manual_url_submission,
)
from app.api.deps import get_current_user, record_audit

router = APIRouter()


@router.post("/cases/{case_id}/discover", response_model=DiscoveryJobResponse, status_code=status.HTTP_202_ACCEPTED)
def trigger_discovery_job(
    case_id: uuid.UUID,
    job_in: DiscoveryJobCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Trigger a public image discovery job across supported social platforms:
    - Queries Meta, X, Reddit, YouTube, and Bluesky connectors
    - Fingerprints candidate thumbnails transiently
    - Ranks candidate matches by perceptual similarity
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized to run discovery on this case")

    if not case.images:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot run discovery on a case with no uploaded fingerprints. Please upload an image first."
        )

    try:
        job, matches = run_discovery_for_case(
            db=db,
            case=case,
            platform_names=job_in.platforms
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Discovery job failed: {str(e)}")

    record_audit(
        db=db,
        action="DISCOVERY_JOB_COMPLETED",
        user_id=current_user.id,
        case_id=case.id,
        details={"job_id": str(job.id), "matches_found": len(matches)},
        request=request
    )

    return job


@router.get("/cases/{case_id}/discovery-jobs", response_model=List[DiscoveryJobResponse])
def list_case_discovery_jobs(
    case_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List historical discovery jobs for a case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    jobs = db.query(DiscoveryJob).filter(DiscoveryJob.case_id == case_id).order_by(DiscoveryJob.created_at.desc()).all()
    return jobs


@router.get("/cases/{case_id}/matches", response_model=List[MatchResponse])
def list_case_matches(
    case_id: uuid.UUID,
    review_status: Optional[str] = Query(None, description="UNREVIEWED, CONFIRMED, REJECTED, UNSURE"),
    confidence_band: Optional[str] = Query(None, description="HIGH, MEDIUM, LOW"),
    min_score: Optional[float] = Query(None, ge=0.0, le=100.0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve ranked matches for a case, sorted by similarity score descending:
    - Supports filtering by human-review status
    - Supports filtering by confidence classification
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    query = db.query(Match).filter(Match.case_id == case_id)

    if review_status:
        query = query.filter(Match.review_status == review_status.upper())
    if confidence_band:
        query = query.filter(Match.confidence_band == confidence_band.upper())
    if min_score is not None:
        query = query.filter(Match.similarity_score >= min_score)

    matches = query.order_by(Match.similarity_score.desc()).all()
    return matches


@router.post("/cases/{case_id}/urls", response_model=List[MatchResponse], status_code=status.HTTP_201_CREATED)
def submit_manual_url(
    case_id: uuid.UUID,
    url_data: ManualUrlSubmission,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a specific suspicious URL for transient media retrieval & fingerprint comparison:
    - Never stores explicit content in logs
    - Produces ranked candidate match records
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if not case.images:
        raise HTTPException(status_code=400, detail="Case has no uploaded images to compare against.")

    try:
        matches = process_manual_url_submission(db=db, case=case, url=url_data.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process URL: {str(e)}")

    record_audit(
        db=db,
        action="MANUAL_URL_VERIFIED",
        user_id=current_user.id,
        case_id=case.id,
        details={"url": url_data.url, "matches_generated": len(matches)},
        request=request
    )

    return matches
