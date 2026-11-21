import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.case import Case
from app.models.case_image import CaseImage
from app.models.discovery_job import DiscoveryJob
from app.models.match import Match
from app.models.evidence import EvidenceItem
from app.models.report import Report, ReportStatusHistory
from app.models.audit_log import AuditLog


def test_models_lifecycle_and_relationships(db_session: Session):
    # 1. Create User
    user = User(
        email="victim.support@example.org",
        hashed_password="hashed_argon2_password_placeholder",
        full_name="Survivor User",
        role="USER",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    assert user.id is not None
    assert user.email == "victim.support@example.org"

    # 2. Create Case
    case = Case(
        user_id=user.id,
        title="Unauthorized Photo Circulation Case",
        description="Private image leaked without consent",
        is_pseudonymous=True,
        pseudonym="Survivor-X",
        status="ACTIVE",
        retain_encrypted_originals=False,
    )
    db_session.add(case)
    db_session.commit()
    db_session.refresh(case)
    assert case.id is not None
    assert case.user.id == user.id

    # 3. Create CaseImage (Fingerprints)
    image = CaseImage(
        case_id=case.id,
        original_filename="sample_source.jpg",
        file_size=102400,
        mime_type="image/jpeg",
        sha256_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        pdq_hash="a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0",
        pdq_quality=95,
        phash="8f8f8f8f8f8f8f8f",
        dhash="0f0f0f0f0f0f0f0f",
        ahash="ffff0000ffff0000",
        is_encrypted=True,
        is_original_deleted=True,
    )
    db_session.add(image)
    db_session.commit()
    db_session.refresh(image)
    assert image.id is not None
    assert image.case_id == case.id

    # 4. Create DiscoveryJob
    job = DiscoveryJob(
        case_id=case.id,
        status="RUNNING",
        platforms_searched=["reddit", "x", "meta", "web"],
        results_count=1,
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)
    assert job.id is not None
    assert "reddit" in job.platforms_searched

    # 5. Create Match
    match = Match(
        case_id=case.id,
        discovery_job_id=job.id,
        case_image_id=image.id,
        platform="REDDIT",
        source_url="https://reddit.com/r/example/post/123",
        author_handle="u/bad_actor",
        similarity_score=94.5,
        confidence_band="HIGH",
        match_reasons=["PDQ distance: 6", "pHash distance: 1"],
        review_status="UNREVIEWED",
    )
    db_session.add(match)
    db_session.commit()
    db_session.refresh(match)
    assert match.id is not None
    assert match.similarity_score == 94.5

    # 6. Create EvidenceItem (with tamper-evident hash chain)
    evidence = EvidenceItem(
        case_id=case.id,
        match_id=match.id,
        evidence_number="EV-2026-0001",
        platform="REDDIT",
        source_url=match.source_url,
        captured_at=datetime.now(timezone.utc),
        content_sha256="abc123def45678901234567890abcdef1234567890abcdef1234567890abcdef",
        similarity_score=94.5,
        metadata_snapshot={"server": "cloudflare", "status": 200},
        previous_evidence_hash="GENESIS",
        evidence_hash="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    )
    db_session.add(evidence)
    db_session.commit()
    db_session.refresh(evidence)
    assert evidence.id is not None
    assert evidence.evidence_number == "EV-2026-0001"

    # 7. Create Report & Status History
    report = Report(
        case_id=case.id,
        report_number="REP-2026-0001",
        report_type="CYBERCRIME_GOV",
        title="Official Complaint for Cybercrime Portal",
        selected_evidence_ids=[str(evidence.id)],
        status="DRAFT",
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    status_history = ReportStatusHistory(
        report_id=report.id,
        previous_status="NONE",
        new_status="DRAFT",
        notes="Initial complaint draft compiled",
        changed_by_user_id=user.id,
    )
    db_session.add(status_history)
    db_session.commit()
    db_session.refresh(report)
    assert len(report.status_history) == 1

    # 8. Create AuditLog
    audit = AuditLog(
        user_id=user.id,
        case_id=case.id,
        action="CASE_CREATED",
        ip_address="127.0.0.1",
        user_agent="pytest-client",
        details={"case_title": case.title},
    )
    db_session.add(audit)
    db_session.commit()
    db_session.refresh(audit)
    assert audit.id is not None
    assert audit.action == "CASE_CREATED"
