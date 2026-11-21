import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.case import Case
from app.models.report import Report, ReportStatusHistory
from app.models.evidence import EvidenceItem
from app.models.user import User
from app.schemas.report import ReportCreate
from app.core.config import settings
from app.reports.pdf_generator import generate_complaint_pdf


def generate_next_report_number(db: Session, case_id: uuid.UUID) -> str:
    """Generate sequential report identifier (e.g., REP-2026-0001)."""
    current_year = datetime.now(timezone.utc).year
    count = db.query(Report).count()
    return f"REP-{current_year}-{(count + 1):04d}"


def _compile_markdown_report_body(
    case: Case,
    report_type: str,
    title: str,
    evidence_items: List[EvidenceItem],
    complainant_name: str,
    recipient_platform: Optional[str],
    custom_notes: Optional[str]
) -> str:
    """Compile formal markdown text body suitable for copying into complaint forms."""
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    lines = [
        f"# FORMAL NOTICE & TAKEDOWN COMPLAINT: {title.upper()}",
        f"**Date & Time**: {now_str}",
        f"**Complainant / Identity**: {complainant_name} {'(Protected Pseudonym)' if case.is_pseudonymous else ''}",
        f"**Case Reference**: {case.id}",
        f"**Target Entity**: {recipient_platform or 'National Cybercrime Portal / Public Intermediary'}",
        "",
        "## 1. Statement of Non-Consensual Imagery Infringement",
        "This formal notice serves as an official complaint regarding the unauthorized publication, distribution, or circulation of non-consensual imagery depicting the complainant. The complainant has NOT given consent for this material to be published, mirrored, or transferred.",
        "",
        "## 2. Applicable Legal Violations",
        "- **Information Technology Act, 2000 (Section 66E)**: Violation of privacy by capturing, publishing, or transmitting images of private area.",
        "- **Information Technology Act, 2000 (Section 67 / 67A)**: Publishing or transmitting obscene material / sexually explicit content in electronic form.",
        "- **IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021 (Rule 3(2)(b))**: Mandates immediate takedown within 24 hours of non-consensual intimate imagery.",
        "- **Bharatiya Nyaya Sanhita (BNS) / Indian Penal Code**: Offenses of Voyeurism (Sec 354C) and Cyberstalking (Sec 354D).",
        "",
        "## 3. Preserved Evidence Schedule & Cryptographic Signatures",
    ]

    for it in evidence_items:
        lines.extend([
            f"### Evidence Ref: {it.evidence_number}",
            f"- **Platform**: {it.platform}",
            f"- **Direct Source URL**: {it.source_url}",
            f"- **Capture Timestamp (UTC)**: {it.captured_at.isoformat()}",
            f"- **Perceptual Match Score**: {it.similarity_score:.1f}%",
            f"- **Content SHA-256**: `{it.content_sha256}`",
            f"- **Cryptographic Chain Block Hash**: `{it.evidence_hash}`",
            "",
        ])

    if custom_notes:
        lines.extend([
            "## 4. Additional Statement from Complainant",
            custom_notes,
            "",
        ])

    lines.extend([
        "## 5. Relief & Remedies Requested",
        "1. Immediate removal, de-indexing, and permanent expungement of the specified URLs.",
        "2. Preservation of uploader server logs, IP logs, and timestamps for cybercrime police referral.",
        "3. Prevention of re-uploading through proactive content hashing.",
    ])

    return "\n".join(lines)


def create_case_report(
    db: Session,
    case: Case,
    report_in: ReportCreate,
    current_user: User
) -> Report:
    """
    Create a consolidated complaint report and build the ReportLab PDF:
    - Validates selected evidence items
    - Formulates legal markdown grievance
    - Generates and writes verifiable PDF to storage
    - Appends initial status history
    """
    evidence_items = (
        db.query(EvidenceItem)
        .filter(EvidenceItem.case_id == case.id, EvidenceItem.id.in_(report_in.selected_evidence_ids))
        .all()
    )

    if not evidence_items:
        raise ValueError("None of the selected evidence items could be found for this case.")

    report_number = generate_next_report_number(db, case.id)
    complainant_name = case.pseudonym if case.is_pseudonymous else (current_user.full_name or "Anonymous Survivor")

    # Generate Markdown complaint text
    report_content = _compile_markdown_report_body(
        case=case,
        report_type=report_in.report_type,
        title=report_in.title,
        evidence_items=evidence_items,
        complainant_name=complainant_name,
        recipient_platform=report_in.recipient_platform,
        custom_notes=report_in.custom_notes
    )

    # Determine storage path for generated PDF
    report_uuid = uuid.uuid4()
    pdf_dest = settings.storage_path / "reports" / str(case.id) / f"{report_uuid}.pdf"

    # Instantiate Report DB Model
    report = Report(
        id=report_uuid,
        case_id=case.id,
        report_number=report_number,
        report_type=report_in.report_type,
        title=report_in.title,
        recipient_platform=report_in.recipient_platform,
        selected_evidence_ids=[str(e.id) for e in evidence_items],
        report_content=report_content,
        pdf_storage_path=str(pdf_dest),
        status="DRAFT",
    )
    db.add(report)
    db.commit()

    # Generate PDF with ReportLab
    generate_complaint_pdf(
        case=case,
        report=report,
        evidence_items=evidence_items,
        output_path=str(pdf_dest)
    )

    # Initial Status History record
    history = ReportStatusHistory(
        report_id=report.id,
        previous_status="NONE",
        new_status="DRAFT",
        notes="Complaint report generated with cryptographic evidence dossier.",
        changed_by_user_id=current_user.id,
    )
    db.add(history)
    db.commit()
    db.refresh(report)

    return report


def update_report_status(
    db: Session,
    report: Report,
    new_status: str,
    notes: Optional[str],
    user_id: uuid.UUID
) -> Report:
    """Transition report status (DRAFT -> SUBMITTED -> ACKNOWLEDGED -> REMOVED)."""
    prev_status = report.status
    report.status = new_status
    report.updated_at = datetime.now(timezone.utc)

    history = ReportStatusHistory(
        report_id=report.id,
        previous_status=prev_status,
        new_status=new_status,
        notes=notes,
        changed_by_user_id=user_id,
    )
    db.add(history)
    db.commit()
    db.refresh(report)
    return report
