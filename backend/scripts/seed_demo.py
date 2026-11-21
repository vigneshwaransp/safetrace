import sys
import os
import uuid
import datetime
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from PIL import Image, ImageDraw

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models import (
    User,
    Case,
    CaseImage,
    DiscoveryJob,
    Match,
    EvidenceItem,
    Report,
    ReportStatusHistory,
    Notification,
)
from app.services.fingerprint import compute_image_fingerprints
from app.services.evidence import create_evidence_from_confirmed_match, verify_evidence_chain
from app.reports.pdf_generator import generate_complaint_pdf


def create_sample_image() -> bytes:
    """Generate a clean synthetic sample image for demo fingerprinting."""
    img = Image.new("RGB", (320, 320), color=(255, 245, 235))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, 280, 280], fill=(26, 58, 58))
    draw.ellipse([80, 80, 240, 240], fill=(255, 77, 139))
    draw.polygon([(160, 90), (220, 220), (100, 220)], fill=(255, 255, 255))
    
    import io
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def seed_database():
    print("--- SafeTrace Demo Database Seeder ---")
    
    # 1. Create all tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if already seeded
        existing_user = db.query(User).filter(User.email == "victim@example.com").first()
        if existing_user:
            print("Demo user 'victim@example.com' already exists. Cleaning existing demo records...")
            # Delete in reverse FK order
            db.query(Notification).delete()
            db.query(ReportStatusHistory).delete()
            db.query(Report).delete()
            db.query(EvidenceItem).delete()
            db.query(Match).delete()
            db.query(DiscoveryJob).delete()
            db.query(CaseImage).delete()
            db.query(Case).delete()
            db.query(User).delete()
            db.commit()

        print("[1/6] Seeding User Accounts...")
        victim = User(
            id=uuid.uuid4(),
            email="victim@example.com",
            hashed_password=get_password_hash("VictimPass123!"),
            full_name="Maya Sharma",
            role="VICTIM",
            is_active=True,
            is_verified=True,
        )
        advocate = User(
            id=uuid.uuid4(),
            email="advocate@example.com",
            hashed_password=get_password_hash("AdvocatePass123!"),
            full_name="Adv. Priya Sharma",
            role="ADVOCATE",
            is_active=True,
            is_verified=True,
        )
        ngo = User(
            id=uuid.uuid4(),
            email="ngo@example.com",
            hashed_password=get_password_hash("NgoPass123!"),
            full_name="Dr. Ananya Roy",
            role="NGO",
            is_active=True,
            is_verified=True,
        )
        db.add_all([victim, advocate, ngo])
        db.commit()
        print(f"  [+] Created Victim: {victim.email}")
        print(f"  [+] Created Advocate: {advocate.email}")
        print(f"  [+] Created NGO: {ngo.email}")

        print("[2/6] Seeding Protected Case...")
        demo_case = Case(
            id=uuid.uuid4(),
            user_id=victim.id,
            title="Unauthorized circulation of morphed images on Reddit and Telegram",
            description=(
                "Private personal photographs originally shared in confidence were morphed and circulated "
                "without consent across public image boards and Telegram channels. Extortion threats received."
            ),
            is_pseudonymous=True,
            pseudonym="Anonymous Victim",
            status="ACTIVE",
            retain_encrypted_originals=False,  # Zero-storage model
        )
        db.add(demo_case)
        db.commit()
        print(f"  [+] Created Case: {demo_case.title}")

        print("[3/6] Computing Real Perceptual Fingerprints...")
        img_bytes = create_sample_image()
        fp = compute_image_fingerprints(img_bytes)

        case_image = CaseImage(
            id=uuid.uuid4(),
            case_id=demo_case.id,
            original_filename="private_reference_portrait.jpg",
            mime_type="image/jpeg",
            file_size=len(img_bytes),
            sha256_hash=fp.sha256,
            pdq_hash=fp.pdq_hash,
            pdq_quality=fp.pdq_quality,
            phash=fp.phash,
            dhash=fp.dhash,
            ahash=fp.ahash,
            is_original_deleted=True,  # Raw media purged
        )
        db.add(case_image)
        db.commit()
        print(f"  [+] Fingerprinted {case_image.original_filename}")
        print(f"    - SHA-256: {fp.sha256[:20]}...")
        print(f"    - PDQ 256-bit Vector: {fp.pdq_hash[:20]}... (Quality: {fp.pdq_quality})")
        print(f"    - Perceptual pHash: {fp.phash}")
        print("    - Status: Original file permanently purged from server (Zero-Knowledge)")

        print("[4/6] Seeding Discovery Jobs & Candidate Matches...")
        job = DiscoveryJob(
            id=uuid.uuid4(),
            case_id=demo_case.id,
            status="COMPLETED",
            platforms_searched=["REDDIT", "X_TWITTER", "META", "WEB"],
            results_count=3,
            started_at=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=2),
            completed_at=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1, minutes=58),
        )
        db.add(job)
        db.commit()

        # Match 1: Reddit (Confirmed)
        match1 = Match(
            id=uuid.uuid4(),
            case_id=demo_case.id,
            case_image_id=case_image.id,
            discovery_job_id=job.id,
            platform="REDDIT",
            source_url="https://reddit.com/r/cyberleaks/comments/xyz123/leaked_images",
            thumbnail_url="https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400",
            author_handle="@anon_distributor",
            post_timestamp=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2),
            similarity_score=96.5,
            confidence_band="HIGH",
            pdq_hash=fp.pdq_hash,
            phash=fp.phash,
            match_reasons=[
                "PDQ Hamming distance 4 (well below threshold 31)",
                "pHash distance 2 (near identical DCT frequencies)",
                "ORB feature keypoint inliers confirmed geometric alignment",
            ],
            review_status="CONFIRMED",
            reviewed_at=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1),
        )

        # Match 2: X (Twitter) (Confirmed)
        match2 = Match(
            id=uuid.uuid4(),
            case_id=demo_case.id,
            case_image_id=case_image.id,
            discovery_job_id=job.id,
            platform="X_TWITTER",
            source_url="https://x.com/anon_distributor/status/198273645",
            thumbnail_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
            author_handle="@dark_feed_in",
            post_timestamp=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1),
            similarity_score=88.2,
            confidence_band="HIGH",
            pdq_hash=fp.pdq_hash,
            phash=fp.phash,
            match_reasons=[
                "PDQ Hamming distance 12 (tight crop of original)",
                "Center-crop spatial pHash matched within distance 3",
            ],
            review_status="CONFIRMED",
            reviewed_at=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=45),
        )

        # Match 3: Open Web (Pending Review)
        match3 = Match(
            id=uuid.uuid4(),
            case_id=demo_case.id,
            case_image_id=case_image.id,
            discovery_job_id=job.id,
            platform="WEB",
            source_url="https://imgpaste.net/raw/ab89cf12.jpg",
            thumbnail_url="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400",
            author_handle="@web_crawler",
            post_timestamp=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=8),
            similarity_score=68.4,
            confidence_band="MEDIUM",
            match_reasons=["Partial multi-scale DCT frequency alignment"],
            review_status="UNREVIEWED",
        )

        db.add_all([match1, match2, match3])
        db.commit()
        print(f"  [+] Added 3 matches across Reddit, X, and Web")

        print("[5/6] Building Tamper-Evident Cryptographic Hash Chain...")
        ev1 = create_evidence_from_confirmed_match(db=db, match=match1)
        ev2 = create_evidence_from_confirmed_match(db=db, match=match2)
        
        is_chain_valid, chain_error = verify_evidence_chain([ev1, ev2])
        print(f"  [+] Block #1: {ev1.evidence_number} (Hash: {ev1.evidence_hash[:16]}...)")
        print(f"  [+] Block #2: {ev2.evidence_number} (Parent: {ev2.previous_evidence_hash[:16]}...)")
        print(f"  [+] Cryptographic Chain Integrity Verified: {is_chain_valid} (Error: {chain_error})")

        print("[6/6] Generating Statutory Report & PDF Dossier...")
        report = Report(
            id=uuid.uuid4(),
            case_id=demo_case.id,
            report_number="REP-2026-0001",
            report_type="PLATFORM_TAKEDOWN",
            title="Statutory Takedown Notice under Rule 3(2)(b) IT Rules 2021",
            recipient_platform="REDDIT",
            status="SUBMITTED",
            selected_evidence_ids=[str(ev1.id), str(ev2.id)],
            report_content=(
                "# FORMAL GRIEVANCE & STATUTORY TAKEDOWN NOTICE\n\n"
                "**Governing Law:** Section 79(3)(b) & Section 66E of the Information Technology Act 2000; "
                "Rule 3(2)(b) of the Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021.\n\n"
                "**Urgency:** Mandatory takedown within 24 hours of notification.\n\n"
                "To: Resident Grievance Officer, Reddit Inc.\n"
                "From: Maya Sharma (Aggrieved Party / Victim of Non-Consensual Imagery)\n\n"
                "Please find enclosed the cryptographic evidence schedule documenting non-consensual image abuse.\n"
            ),
        )
        db.add(report)
        db.commit()

        # Generate the PDF file
        pdf_filename = f"SafeTrace_Dossier_{report.report_number}.pdf"
        output_pdf_path = str(settings.storage_path / pdf_filename)
        generate_complaint_pdf(
            case=demo_case,
            report=report,
            evidence_items=[ev1, ev2],
            output_path=output_pdf_path,
        )
        report.pdf_storage_path = output_pdf_path
        db.commit()

        # Report Status History
        hist1 = ReportStatusHistory(
            id=uuid.uuid4(),
            report_id=report.id,
            previous_status="INITIAL",
            new_status="DRAFT",
            notes="Statutory notice compiled with 2 evidence blocks.",
        )
        hist2 = ReportStatusHistory(
            id=uuid.uuid4(),
            report_id=report.id,
            previous_status="DRAFT",
            new_status="SUBMITTED",
            notes="Transmitted via official Reddit Grievance channel. Ticket REDDIT-TKT-99214 acknowledged.",
        )
        db.add_all([hist1, hist2])

        # Notifications
        notif1 = Notification(
            id=uuid.uuid4(),
            user_id=victim.id,
            case_id=demo_case.id,
            title="Takedown Grievance Submitted",
            message="Reddit Grievance Ticket #REDDIT-TKT-99214 has been recorded. 24/7 Celery Beat liveness scan active.",
            notification_type="INFO",
            is_read=False,
        )
        db.add(notif1)
        db.commit()

        print(f"  [+] Created ReportLab PDF Dossier: {pdf_filename}")
        print(f"  [+] Created Grievance Record: {report.report_number} (Status: {report.status})")
        print("\n=== Demo Seed Successfully Completed! ===")
        print("Login credentials for demo:")
        print("  - Victim:   victim@example.com   / VictimPass123!")
        print("  - Advocate: advocate@example.com / AdvocatePass123!")
        print("  - NGO:      ngo@example.com      / NgoPass123!")
        print("==========================================\n")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
