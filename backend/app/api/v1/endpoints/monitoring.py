from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.services.monitoring import (
    run_monitoring_cycle,
    check_url_liveness,
)
from app.api.deps import get_current_user

router = APIRouter()


class UrlCheckRequest(BaseModel):
    url: str


class UrlCheckResponse(BaseModel):
    url: str
    is_live: bool
    status_code: int
    details: str


@router.post("/run-cycle")
def trigger_monitoring_cycle(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Manually trigger an automated monitoring cycle:
    - Scans submitted/acknowledged reports
    - Checks live URLs for deletion or reappearance
    - Updates report statuses and emits user notifications
    """
    results = run_monitoring_cycle(db=db)
    return results


@router.post("/check-url", response_model=UrlCheckResponse)
def check_single_url(
    req: UrlCheckRequest,
    current_user: User = Depends(get_current_user),
):
    """Inspect liveness of a specific URL."""
    is_live, status_code, details = check_url_liveness(req.url)
    return UrlCheckResponse(
        url=req.url,
        is_live=is_live,
        status_code=status_code,
        details=details,
    )
