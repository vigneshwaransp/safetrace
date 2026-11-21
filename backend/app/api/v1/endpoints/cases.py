import os
import uuid
import hashlib
from typing import List
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.case import Case
from app.models.case_image import CaseImage
from app.schemas.case import (
    CaseCreate,
    CaseUpdate,
    CaseResponse,
    CaseDetailResponse,
)
from app.schemas.image import CaseImageResponse, ImagePurgeResponse
from app.core.config import settings
from app.core.security import encrypt_bytes
from app.services.fingerprint import compute_image_fingerprints
from app.api.deps import get_current_user, record_audit

router = APIRouter()


@router.post("", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
def create_case(
    case_in: CaseCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new confidential case container."""
    case = Case(
        user_id=current_user.id,
        title=case_in.title,
        description=case_in.description,
        is_pseudonymous=case_in.is_pseudonymous,
        pseudonym=case_in.pseudonym if case_in.is_pseudonymous else None,
        status="ACTIVE",
        retain_encrypted_originals=case_in.retain_encrypted_originals,
    )
    db.add(case)
    db.commit()
    db.refresh(case)

    record_audit(
        db=db,
        action="CASE_CREATED",
        user_id=current_user.id,
        case_id=case.id,
        details={"title": case.title, "pseudonymous": case.is_pseudonymous},
        request=request
    )

    return CaseResponse(
        id=case.id,
        user_id=case.user_id,
        title=case.title,
        description=case.description,
        is_pseudonymous=case.is_pseudonymous,
        pseudonym=case.pseudonym,
        status=case.status,
        retain_encrypted_originals=case.retain_encrypted_originals,
        created_at=case.created_at,
        updated_at=case.updated_at,
        image_count=0,
        matches_count=0,
    )


@router.get("", response_model=List[CaseResponse])
def list_cases(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List cases accessible by the current user."""
    if current_user.role in ["ADMIN", "NGO"]:
        cases = db.query(Case).order_by(Case.created_at.desc()).all()
    else:
        cases = db.query(Case).filter(Case.user_id == current_user.id).order_by(Case.created_at.desc()).all()

    results = []
    for c in cases:
        results.append(
            CaseResponse(
                id=c.id,
                user_id=c.user_id,
                title=c.title,
                description=c.description,
                is_pseudonymous=c.is_pseudonymous,
                pseudonym=c.pseudonym,
                status=c.status,
                retain_encrypted_originals=c.retain_encrypted_originals,
                created_at=c.created_at,
                updated_at=c.updated_at,
                image_count=len(c.images),
                matches_count=len(c.matches),
            )
        )
    return results


@router.get("/{case_id}", response_model=CaseDetailResponse)
def get_case_detail(
    case_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve detailed case view including registered fingerprints."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role not in ["ADMIN", "NGO"]:
        raise HTTPException(status_code=403, detail="Not authorized to access this case")

    return CaseDetailResponse(
        id=case.id,
        user_id=case.user_id,
        title=case.title,
        description=case.description,
        is_pseudonymous=case.is_pseudonymous,
        pseudonym=case.pseudonym,
        status=case.status,
        retain_encrypted_originals=case.retain_encrypted_originals,
        created_at=case.created_at,
        updated_at=case.updated_at,
        image_count=len(case.images),
        matches_count=len(case.matches),
        images=[CaseImageResponse.model_validate(img) for img in case.images],
    )


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def purge_case(
    case_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Full purge: Permanently delete a case, all fingerprints, and associated storage files."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized to purge this case")

    # Clean up any stored files on disk
    for img in case.images:
        if img.storage_path and os.path.exists(img.storage_path):
            try:
                os.remove(img.storage_path)
            except OSError:
                pass

    record_audit(
        db=db,
        action="CASE_PURGED_PERMANENTLY",
        user_id=current_user.id,
        case_id=case.id,
        details={"case_title": case.title},
        request=request
    )

    db.delete(case)
    db.commit()
    return None


@router.post("/{case_id}/images", response_model=CaseImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_case_image(
    case_id: uuid.UUID,
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Secure Image Upload:
    - Verifies file size limit
    - Computes exact SHA-256 fingerprint
    - Applies AES-256 encryption at rest
    - If retain_encrypted_originals=False, deletes original content immediately (zero-knowledge)
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized to upload to this case")

    raw_bytes = await file.read()
    file_size = len(raw_bytes)
    if file_size > settings.UPLOAD_MAX_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size ({settings.UPLOAD_MAX_BYTES} bytes)"
        )
    if file_size == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    # Compute exact SHA-256 and perceptual fingerprints (PDQ, pHash, dHash, aHash)
    sha256_hash = hashlib.sha256(raw_bytes).hexdigest()
    fp = None
    try:
        fp = compute_image_fingerprints(raw_bytes)
    except Exception:
        # Fallback if corrupted image format
        pass

    storage_path = None
    is_original_deleted = True

    # If user explicitly opted into retaining encrypted originals, save AES-256 ciphertext
    if case.retain_encrypted_originals:
        encrypted_data = encrypt_bytes(raw_bytes)
        case_storage_dir = settings.storage_path / "encrypted" / str(case.id)
        case_storage_dir.mkdir(parents=True, exist_ok=True)
        
        file_uuid = uuid.uuid4()
        file_dest = case_storage_dir / f"{file_uuid}.enc"
        file_dest.write_bytes(encrypted_data)
        storage_path = str(file_dest)
        is_original_deleted = False

    case_image = CaseImage(
        case_id=case.id,
        original_filename=file.filename or "unknown.jpg",
        file_size=file_size,
        mime_type=file.content_type or "image/jpeg",
        sha256_hash=sha256_hash,
        pdq_hash=fp.pdq_hash if fp else None,
        pdq_quality=fp.pdq_quality if fp else None,
        phash=fp.phash if fp else None,
        dhash=fp.dhash if fp else None,
        ahash=fp.ahash if fp else None,
        keypoints_summary=fp.keypoints_summary if fp else None,
        storage_path=storage_path,
        is_encrypted=True,
        is_original_deleted=is_original_deleted,
    )
    db.add(case_image)
    db.commit()
    db.refresh(case_image)

    record_audit(
        db=db,
        action="IMAGE_FINGERPRINTED",
        user_id=current_user.id,
        case_id=case.id,
        details={
            "image_id": str(case_image.id),
            "sha256": sha256_hash,
            "original_deleted": is_original_deleted
        },
        request=request
    )

    return case_image


@router.post("/{case_id}/images/{image_id}/purge", response_model=ImagePurgeResponse)
def purge_original_image(
    case_id: uuid.UUID,
    image_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    One-click permanent deletion of any retained original file from disk.
    Preserves perceptual fingerprints and SHA-256 for ongoing public monitoring.
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized")

    image = db.query(CaseImage).filter(CaseImage.id == image_id, CaseImage.case_id == case.id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image record not found")

    if image.storage_path and os.path.exists(image.storage_path):
        try:
            os.remove(image.storage_path)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file from disk: {str(e)}")

    image.storage_path = None
    image.is_original_deleted = True
    db.commit()

    record_audit(
        db=db,
        action="ORIGINAL_IMAGE_PERMANENTLY_PURGED",
        user_id=current_user.id,
        case_id=case.id,
        details={"image_id": str(image.id), "sha256": image.sha256_hash},
        request=request
    )

    return ImagePurgeResponse(
        image_id=image.id,
        message="Original file permanently deleted from disk. Fingerprint retained for active protection.",
        is_original_deleted=True,
        sha256_retained=image.sha256_hash
    )
