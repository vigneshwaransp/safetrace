import json
import uuid
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from app.models.case import Case
from app.models.match import Match
from app.models.evidence import EvidenceItem


def _normalize_datetime_string(dt: datetime) -> str:
    """Normalize datetime to consistent UTC format: YYYY-MM-DDTHH:MM:SS.ffffffZ."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def compute_canonical_evidence_hash(
    evidence_number: str,
    case_id: uuid.UUID,
    match_id: uuid.UUID,
    platform: str,
    source_url: str,
    captured_at_dt: datetime,
    content_sha256: str,
    similarity_score: float,
    previous_evidence_hash: str
) -> str:
    """
    Compute a deterministic SHA-256 hash across canonical evidence properties
    bound cryptographically to the preceding evidence record's hash (blockchain-style chain).
    """
    payload = {
        "evidence_number": evidence_number,
        "case_id": str(case_id),
        "match_id": str(match_id),
        "platform": platform.upper(),
        "source_url": source_url.strip(),
        "captured_at": _normalize_datetime_string(captured_at_dt),
        "content_sha256": content_sha256.lower(),
        "similarity_score": round(similarity_score, 2),
        "previous_evidence_hash": previous_evidence_hash,
    }
    canonical_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def generate_next_evidence_number(db: Session, case_id: uuid.UUID) -> str:
    """Generate sequential evidence reference (e.g. EV-2026-0001)."""
    current_year = datetime.now(timezone.utc).year
    count = db.query(EvidenceItem).filter(EvidenceItem.case_id == case_id).count()
    return f"EV-{current_year}-{(count + 1):04d}"


def create_evidence_from_confirmed_match(
    db: Session,
    match: Match,
    screenshot_path: Optional[str] = None
) -> EvidenceItem:
    """
    Create a new tamper-evident evidence record from a confirmed match:
    - Finds the latest evidence item in the case to link to previous_evidence_hash.
    - Generates sequential evidence number.
    - Captures immutable timestamp and content SHA-256.
    - Computes cryptographic evidence hash.
    """
    existing = db.query(EvidenceItem).filter(EvidenceItem.match_id == match.id).first()
    if existing:
        return existing

    latest_evidence = (
        db.query(EvidenceItem)
        .filter(EvidenceItem.case_id == match.case_id)
        .order_by(EvidenceItem.created_at.desc())
        .first()
    )
    previous_hash = latest_evidence.evidence_hash if latest_evidence else "GENESIS"

    evidence_number = generate_next_evidence_number(db, match.case_id)
    captured_at = datetime.now(timezone.utc)
    content_sha256 = match.sha256_hash or hashlib.sha256(match.source_url.encode()).hexdigest()

    evidence_hash = compute_canonical_evidence_hash(
        evidence_number=evidence_number,
        case_id=match.case_id,
        match_id=match.id,
        platform=match.platform,
        source_url=match.source_url,
        captured_at_dt=captured_at,
        content_sha256=content_sha256,
        similarity_score=match.similarity_score,
        previous_evidence_hash=previous_hash,
    )

    metadata_snapshot = {
        "author_handle": match.author_handle,
        "post_timestamp": match.post_timestamp.isoformat() if match.post_timestamp else None,
        "thumbnail_url": match.thumbnail_url,
        "media_url": match.media_url,
        "confidence_band": match.confidence_band,
        "match_reasons": match.match_reasons,
        "verified_at": _normalize_datetime_string(captured_at),
    }

    item = EvidenceItem(
        case_id=match.case_id,
        match_id=match.id,
        evidence_number=evidence_number,
        platform=match.platform,
        source_url=match.source_url,
        captured_at=captured_at,
        content_sha256=content_sha256,
        screenshot_storage_path=screenshot_path,
        similarity_score=match.similarity_score,
        metadata_snapshot=metadata_snapshot,
        previous_evidence_hash=previous_hash,
        evidence_hash=evidence_hash,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def verify_evidence_chain(evidence_items: List[EvidenceItem]) -> Tuple[bool, Optional[str]]:
    """
    Verify the cryptographic integrity of an append-only evidence log:
    - Verifies that previous_evidence_hash matches the preceding block.
    - Re-computes canonical hash and compares to evidence_hash.
    - Returns (True, None) if completely intact, or (False, reason) if tampered with.
    """
    if not evidence_items:
        return True, None

    sorted_items = sorted(evidence_items, key=lambda x: x.created_at)

    expected_prev = "GENESIS"
    for idx, item in enumerate(sorted_items):
        if item.previous_evidence_hash != expected_prev:
            return False, f"Broken link at {item.evidence_number}: expected previous hash {expected_prev}, got {item.previous_evidence_hash}"

        recomputed = compute_canonical_evidence_hash(
            evidence_number=item.evidence_number,
            case_id=item.case_id,
            match_id=item.match_id,
            platform=item.platform,
            source_url=item.source_url,
            captured_at_dt=item.captured_at,
            content_sha256=item.content_sha256,
            similarity_score=item.similarity_score,
            previous_evidence_hash=item.previous_evidence_hash,
        )

        if recomputed != item.evidence_hash:
            return False, f"Tampered record at {item.evidence_number}: payload hash mismatch"

        expected_prev = item.evidence_hash

    return True, None
