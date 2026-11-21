import io
import os
import uuid
import hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.case import Case
from app.models.case_image import CaseImage
from app.models.audit_log import AuditLog
from app.core.security import decrypt_bytes


def _get_auth_headers(client: TestClient, email: str = "case.user@example.com") -> dict:
    password = "SafePassword123!"
    client.post("/api/v1/auth/register", json={"email": email, "password": password})
    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_and_list_cases(client: TestClient):
    headers = _get_auth_headers(client, "creator@example.com")

    # Create Case
    payload = {
        "title": "Unauthorized Leak on Imageboard",
        "description": "Image reposted without consent",
        "is_pseudonymous": True,
        "pseudonym": "Survivor-Rose",
        "retain_encrypted_originals": False,
    }
    create_resp = client.post("/api/v1/cases", json=payload, headers=headers)
    assert create_resp.status_code == 201
    case_data = create_resp.json()
    assert case_data["title"] == payload["title"]
    assert case_data["pseudonym"] == "Survivor-Rose"
    assert case_data["retain_encrypted_originals"] is False

    case_id = case_data["id"]

    # List Cases
    list_resp = client.get("/api/v1/cases", headers=headers)
    assert list_resp.status_code == 200
    cases = list_resp.json()
    assert len(cases) >= 1
    assert any(c["id"] == case_id for c in cases)

    # Detail View
    detail_resp = client.get(f"/api/v1/cases/{case_id}", headers=headers)
    assert detail_resp.status_code == 200
    assert detail_resp.json()["id"] == case_id


def test_upload_image_zero_knowledge_deletion(client: TestClient, db_session: Session):
    """Test default zero-knowledge mode: original file is purged immediately after hashing."""
    headers = _get_auth_headers(client, "zeroknowledge@example.com")
    case_resp = client.post("/api/v1/cases", json={"title": "Zero Knowledge Case", "retain_encrypted_originals": False}, headers=headers)
    case_id = case_resp.json()["id"]

    # Prepare sample image bytes
    sample_bytes = b"fake-jpeg-raw-image-bytes-for-testing-123456789"
    expected_sha256 = hashlib.sha256(sample_bytes).hexdigest()

    file_payload = {
        "file": ("evidence.jpg", io.BytesIO(sample_bytes), "image/jpeg")
    }

    upload_resp = client.post(f"/api/v1/cases/{case_id}/images", files=file_payload, headers=headers)
    assert upload_resp.status_code == 201
    data = upload_resp.json()
    assert data["sha256_hash"] == expected_sha256
    assert data["is_original_deleted"] is True

    # Verify database record
    db_img = db_session.query(CaseImage).filter(CaseImage.id == uuid.UUID(data["id"])).first()
    assert db_img is not None
    assert db_img.storage_path is None
    assert db_img.is_original_deleted is True


def test_upload_image_encrypted_retention_and_purge(client: TestClient, db_session: Session):
    """Test opt-in encrypted retention: original is stored encrypted with AES-256, then one-click purged."""
    headers = _get_auth_headers(client, "retention@example.com")
    case_resp = client.post("/api/v1/cases", json={"title": "Retained Case", "retain_encrypted_originals": True}, headers=headers)
    case_id = case_resp.json()["id"]

    raw_bytes = b"strictly-confidential-survivor-image-content-bytes-999"
    expected_sha256 = hashlib.sha256(raw_bytes).hexdigest()

    file_payload = {
        "file": ("confidential.png", io.BytesIO(raw_bytes), "image/png")
    }

    upload_resp = client.post(f"/api/v1/cases/{case_id}/images", files=file_payload, headers=headers)
    assert upload_resp.status_code == 201
    img_data = upload_resp.json()
    assert img_data["is_original_deleted"] is False

    image_id = img_data["id"]
    db_img = db_session.query(CaseImage).filter(CaseImage.id == uuid.UUID(image_id)).first()
    assert db_img.storage_path is not None
    assert os.path.exists(db_img.storage_path)

    # Verify that the saved file is AES ciphertext and can be decrypted to match raw_bytes
    ciphertext = Path(db_img.storage_path).read_bytes()
    assert ciphertext != raw_bytes
    decrypted = decrypt_bytes(ciphertext)
    assert decrypted == raw_bytes

    # Now test One-Click Permanent Purge
    purge_resp = client.post(f"/api/v1/cases/{case_id}/images/{image_id}/purge", headers=headers)
    assert purge_resp.status_code == 200
    purge_data = purge_resp.json()
    assert purge_data["is_original_deleted"] is True
    assert purge_data["sha256_retained"] == expected_sha256

    # Verify file is deleted from disk
    assert not os.path.exists(db_img.storage_path if db_img.storage_path else "dummy")
    db_session.refresh(db_img)
    assert db_img.storage_path is None
    assert db_img.is_original_deleted is True

    # Audit log check
    audit = db_session.query(AuditLog).filter(AuditLog.action == "ORIGINAL_IMAGE_PERMANENTLY_PURGED").first()
    assert audit is not None


def test_full_case_purge(client: TestClient, db_session: Session):
    headers = _get_auth_headers(client, "purgeme@example.com")
    case_resp = client.post("/api/v1/cases", json={"title": "Case to Purge"}, headers=headers)
    case_id = case_resp.json()["id"]

    # Delete case
    delete_resp = client.delete(f"/api/v1/cases/{case_id}", headers=headers)
    assert delete_resp.status_code == 204

    # Confirm case is gone
    get_resp = client.get(f"/api/v1/cases/{case_id}", headers=headers)
    assert get_resp.status_code == 404
