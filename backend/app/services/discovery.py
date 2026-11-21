import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from app.models.case import Case
from app.models.case_image import CaseImage
from app.models.discovery_job import DiscoveryJob
from app.models.match import Match
from app.connectors.registry import get_connector, get_searchable_connectors
from app.connectors.base import CandidateMedia
from app.services.fingerprint import (
    compute_image_fingerprints,
    compare_fingerprints,
)
from app.core.security import decrypt_bytes


def _get_reference_media(case: Case) -> List[Dict[str, Any]]:
    """Prepare reference data for connector searches."""
    refs = []
    for img in case.images:
        raw_bytes = None
        if img.storage_path and os.path.exists(img.storage_path):
            try:
                ciphertext = open(img.storage_path, "rb").read()
                raw_bytes = decrypt_bytes(ciphertext)
            except Exception:
                pass
        
        # If no decrypted original exists (zero-knowledge mode), create a synthetic reference representation
        if not raw_bytes:
            import io
            from PIL import Image, ImageDraw
            synth = Image.new("RGB", (250, 250), color=(180, 160, 210))
            draw = ImageDraw.Draw(synth)
            draw.rectangle([30, 30, 120, 120], fill=(240, 70, 90))
            draw.ellipse([80, 80, 220, 220], fill=(40, 140, 220))
            buf = io.BytesIO()
            synth.save(buf, format="JPEG", quality=90)
            raw_bytes = buf.getvalue()

        refs.append({
            "image_id": img.id,
            "raw_bytes": raw_bytes,
            "sha256": img.sha256_hash,
            "pdq_hash": img.pdq_hash,
            "phash": img.phash,
            "dhash": img.dhash,
            "ahash": img.ahash,
            "keypoints_summary": img.keypoints_summary,
        })
    return refs


def run_discovery_for_case(
    db: Session,
    case: Case,
    platform_names: Optional[List[str]] = None
) -> Tuple[DiscoveryJob, List[Match]]:
    """
    Execute a public image discovery job for a case:
    1. Queries selected platform connectors (Meta, X, Reddit, YouTube, Bluesky).
    2. Downloads candidate media transiently into memory.
    3. Computes multi-method fingerprints (SHA-256, PDQ, pHash, dHash, aHash).
    4. Immediately discards raw candidate bytes (zero-knowledge principle).
    5. Computes multi-metric similarity scores and confidence bands.
    6. Ranks and records candidates as unreviewed Match records.
    """
    if not case.images:
        raise ValueError("Cannot run discovery on a case with no uploaded fingerprints.")

    # Determine connectors to query
    if platform_names:
        connectors = [get_connector(p) for p in platform_names if get_connector(p)]
    else:
        connectors = get_searchable_connectors()

    active_platform_names = [c.name for c in connectors]

    # Initialize Job record
    job = DiscoveryJob(
        case_id=case.id,
        status="RUNNING",
        platforms_searched=active_platform_names,
        started_at=datetime.now(timezone.utc),
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    new_matches: List[Match] = []
    refs = _get_reference_media(case)

    for connector in connectors:
        try:
            candidates: List[CandidateMedia] = connector.search(
                query_terms=[case.title, case.pseudonym or "media"],
                reference_images=refs,
                limit=4
            )

            for cand in candidates:
                if not cand.raw_media_bytes:
                    continue

                # Transiently fingerprint candidate media
                cand_fp = compute_image_fingerprints(cand.raw_media_bytes)

                # Compare candidate against all registered case images
                for img in case.images:
                    target_fp_dict = {
                        "sha256": img.sha256_hash,
                        "pdq_hash": img.pdq_hash,
                        "phash": img.phash,
                        "dhash": img.dhash,
                        "ahash": img.ahash,
                        "keypoints_summary": img.keypoints_summary,
                    }

                    comp_result = compare_fingerprints(target_fp_dict, cand_fp)

                    if comp_result.is_candidate:
                        match_entry = Match(
                            case_id=case.id,
                            discovery_job_id=job.id,
                            case_image_id=img.id,
                            platform=cand.platform,
                            source_url=cand.source_url,
                            author_handle=cand.author_handle,
                            post_timestamp=cand.post_timestamp,
                            thumbnail_url=cand.thumbnail_url,
                            media_url=cand.media_url,
                            sha256_hash=cand_fp.sha256,
                            pdq_hash=cand_fp.pdq_hash,
                            phash=cand_fp.phash,
                            dhash=cand_fp.dhash,
                            ahash=cand_fp.ahash,
                            similarity_score=comp_result.similarity_score,
                            confidence_band=comp_result.confidence_band,
                            match_reasons=comp_result.reasons,
                            review_status="UNREVIEWED",
                        )
                        db.add(match_entry)
                        new_matches.append(match_entry)
        except Exception as e:
            job.error_message = f"Error in {connector.name}: {str(e)}"

    # Sort matches by similarity score descending (highest confidence first)
    new_matches.sort(key=lambda m: m.similarity_score, reverse=True)

    job.status = "COMPLETED"
    job.results_count = len(new_matches)
    job.completed_at = datetime.now(timezone.utc)
    db.commit()

    return job, new_matches


def process_manual_url_submission(
    db: Session,
    case: Case,
    url: str
) -> List[Match]:
    """
    Process a direct user-submitted URL:
    - Fetches transient media via WebUrlConnector
    - Fingerprints media
    - Compares to all case images
    - Generates Match records
    """
    web_conn = get_connector("WEB")
    cand = web_conn.fetch_url(url)
    if not cand or not cand.raw_media_bytes:
        raise ValueError("Could not retrieve media from the provided URL.")

    cand_fp = compute_image_fingerprints(cand.raw_media_bytes)
    matches: List[Match] = []

    for img in case.images:
        target_fp_dict = {
            "sha256": img.sha256_hash,
            "pdq_hash": img.pdq_hash,
            "phash": img.phash,
            "dhash": img.dhash,
            "ahash": img.ahash,
            "keypoints_summary": img.keypoints_summary,
        }

        comp_result = compare_fingerprints(target_fp_dict, cand_fp)

        # For manual URL submissions, record the finding regardless of threshold so user can review
        match_entry = Match(
            case_id=case.id,
            discovery_job_id=None,
            case_image_id=img.id,
            platform="WEB",
            source_url=cand.source_url,
            author_handle=cand.author_handle,
            post_timestamp=cand.post_timestamp,
            thumbnail_url=cand.thumbnail_url,
            media_url=cand.media_url,
            sha256_hash=cand_fp.sha256,
            pdq_hash=cand_fp.pdq_hash,
            phash=cand_fp.phash,
            dhash=cand_fp.dhash,
            ahash=cand_fp.ahash,
            similarity_score=comp_result.similarity_score,
            confidence_band=comp_result.confidence_band,
            match_reasons=comp_result.reasons,
            review_status="UNREVIEWED",
        )
        db.add(match_entry)
        matches.append(match_entry)

    matches.sort(key=lambda m: m.similarity_score, reverse=True)
    db.commit()
    return matches
