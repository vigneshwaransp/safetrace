import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.case import Case
from app.models.report import Report
from app.schemas.report import (
    ReportCreate,
    ReportStatusUpdate,
    ReportResponse,
)
from app.services.reports import (
    create_case_report,
    update_report_status,
)
from app.api.deps import get_current_user, record_audit

router = APIRouter()


@router.post("/cases/{case_id}/reports", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def generate_report(
    case_id: uuid.UUID,
    report_in: ReportCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a Consolidated Evidence & Complaint Report:
    - Assembles selected confirmed evidence items into a legal grievance document
    - Generates a court-admissible ReportLab PDF containing the cryptographic hash chain
    - Prepares step-by-step guidance for cybercrime.gov.in and platform submission
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        report = create_case_report(
            db=db,
            case=case,
            report_in=report_in,
            current_user=current_user
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report PDF: {str(e)}")

    record_audit(
        db=db,
        action="REPORT_GENERATED",
        user_id=current_user.id,
        case_id=case.id,
        details={
            "report_id": str(report.id),
            "report_number": report.report_number,
            "report_type": report.report_type,
            "evidence_count": len(report.selected_evidence_ids)
        },
        request=request
    )

    return ReportResponse(
        id=report.id,
        case_id=report.case_id,
        report_number=report.report_number,
        report_type=report.report_type,
        title=report.title,
        recipient_platform=report.recipient_platform,
        selected_evidence_ids=report.selected_evidence_ids,
        report_content=report.report_content,
        pdf_available=bool(report.pdf_storage_path and os.path.exists(report.pdf_storage_path)),
        status=report.status,
        created_at=report.created_at,
        updated_at=report.updated_at,
        status_history=report.status_history,
    )


@router.get("/cases/{case_id}/reports", response_model=List[ReportResponse])
def list_case_reports(
    case_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all generated reports for a specific case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    reports = db.query(Report).filter(Report.case_id == case_id).order_by(Report.created_at.desc()).all()
    results = []
    for r in reports:
        results.append(
            ReportResponse(
                id=r.id,
                case_id=r.case_id,
                report_number=r.report_number,
                report_type=r.report_type,
                title=r.title,
                recipient_platform=r.recipient_platform,
                selected_evidence_ids=r.selected_evidence_ids,
                report_content=r.report_content,
                pdf_available=bool(r.pdf_storage_path and os.path.exists(r.pdf_storage_path)),
                status=r.status,
                created_at=r.created_at,
                updated_at=r.updated_at,
                status_history=r.status_history,
            )
        )
    return results


@router.get("/reports/{report_id}", response_model=ReportResponse)
def get_report_detail(
    report_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve details, status history, and markdown text for a specific report."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    case = db.query(Case).filter(Case.id == report.case_id).first()
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    return ReportResponse(
        id=report.id,
        case_id=report.case_id,
        report_number=report.report_number,
        report_type=report.report_type,
        title=report.title,
        recipient_platform=report.recipient_platform,
        selected_evidence_ids=report.selected_evidence_ids,
        report_content=report.report_content,
        pdf_available=bool(report.pdf_storage_path and os.path.exists(report.pdf_storage_path)),
        status=report.status,
        created_at=report.created_at,
        updated_at=report.updated_at,
        status_history=report.status_history,
    )


@router.get("/reports/{report_id}/pdf")
def download_report_pdf(
    report_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download the generated ReportLab PDF evidence document."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    case = db.query(Case).filter(Case.id == report.case_id).first()
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if not report.pdf_storage_path or not os.path.exists(report.pdf_storage_path):
        raise HTTPException(status_code=404, detail="PDF report file not found on disk")

    filename = f"SafeTrace_{report.report_number}.pdf"
    return FileResponse(
        path=report.pdf_storage_path,
        media_type="application/pdf",
        filename=filename,
    )


@router.patch("/reports/{report_id}/status", response_model=ReportResponse)
def change_report_status(
    report_id: uuid.UUID,
    status_update: ReportStatusUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update progress status for a takedown report:
    - Status cycle: DRAFT -> SUBMITTED -> ACKNOWLEDGED -> REMOVED / REJECTED / REAPPEARED
    - Records audit log and appends to status history timeline
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    case = db.query(Case).filter(Case.id == report.case_id).first()
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    valid_statuses = ["DRAFT", "SUBMITTED", "ACKNOWLEDGED", "REMOVED", "REJECTED", "REAPPEARED"]
    normalized_status = status_update.status.upper()
    if normalized_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{status_update.status}'. Valid choices are: {', '.join(valid_statuses)}"
        )

    updated_report = update_report_status(
        db=db,
        report=report,
        new_status=normalized_status,
        notes=status_update.notes,
        user_id=current_user.id
    )

    record_audit(
        db=db,
        action="REPORT_STATUS_CHANGED",
        user_id=current_user.id,
        case_id=case.id,
        details={
            "report_id": str(report.id),
            "new_status": normalized_status,
            "notes": status_update.notes
        },
        request=request
    )

    return ReportResponse(
        id=updated_report.id,
        case_id=updated_report.case_id,
        report_number=updated_report.report_number,
        report_type=updated_report.report_type,
        title=updated_report.title,
        recipient_platform=updated_report.recipient_platform,
        selected_evidence_ids=updated_report.selected_evidence_ids,
        report_content=updated_report.report_content,
        pdf_available=bool(updated_report.pdf_storage_path and os.path.exists(updated_report.pdf_storage_path)),
        status=updated_report.status,
        created_at=updated_report.created_at,
        updated_at=updated_report.updated_at,
        status_history=updated_report.status_history,
    )
