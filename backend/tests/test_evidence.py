import io
import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.match import Match
from app.models.evidence import EvidenceItem
from tests.test_cases import _get_auth_headers
from tests.test_fingerprint import _generate_test_image


def _setup_case_with_matches(client: TestClient, email: str) -> tuple[dict, str, list]:
    headers = _get_auth_headers(client, email)
    case_resp = client.post("/api/v1/cases", json={"title": "Evidence Verification Case"}, headers=headers)
    case_id = case_resp.json()["id"]

    img_bytes = _generate_test_image((300, 300))
    client.post(
        f"/api/v1/cases/{case_id}/images",
        files={"file": ("target.jpg", io.BytesIO(img_bytes), "image/jpeg")},
        headers=headers
    )

    client.post(f"/api/v1/cases/{case_id}/discover", json={}, headers=headers)
    matches_resp = client.get(f"/api/v1/cases/{case_id}/matches", headers=headers)
    matches = matches_resp.json()
    return headers, case_id, matches


def test_human_in_the_loop_confirm_creates_evidence(client: TestClient):
    headers, case_id, matches = _setup_case_with_matches(client, "hitl.confirm@example.com")
    assert len(matches) >= 1
    target_match = matches[0]
    match_id = target_match["id"]

    # Confirm match
    review_payload = {
        "review_status": "CONFIRMED",
        "reviewer_notes": "Verified unauthorized copy of confidential image."
    }
    patch_resp = client.patch(f"/api/v1/matches/{match_id}", json=review_payload, headers=headers)
    assert patch_resp.status_code == 200
    updated_match = patch_resp.json()
    assert updated_match["review_status"] == "CONFIRMED"
    assert updated_match["reviewer_notes"] == review_payload["reviewer_notes"]

    # Verify Evidence Item in Vault
    vault_resp = client.get(f"/api/v1/cases/{case_id}/evidence", headers=headers)
    assert vault_resp.status_code == 200
    vault = vault_resp.json()
    assert vault["total_items"] == 1
    assert vault["is_chain_valid"] is True

    evidence_item = vault["items"][0]
    assert evidence_item["match_id"] == match_id
    assert evidence_item["previous_evidence_hash"] == "GENESIS"
    assert len(evidence_item["evidence_hash"]) == 64
    assert evidence_item["evidence_number"].startswith("EV-")


def test_match_rejection_does_not_create_evidence(client: TestClient):
    headers, case_id, matches = _setup_case_with_matches(client, "hitl.reject@example.com")
    assert len(matches) >= 1
    match_id = matches[0]["id"]

    # Reject match
    review_payload = {
        "review_status": "REJECTED",
        "reviewer_notes": "False positive; unrelated generic image."
    }
    patch_resp = client.patch(f"/api/v1/matches/{match_id}", json=review_payload, headers=headers)
    assert patch_resp.status_code == 200
    assert patch_resp.json()["review_status"] == "REJECTED"

    # Verify no evidence item created
    vault_resp = client.get(f"/api/v1/cases/{case_id}/evidence", headers=headers)
    assert vault_resp.status_code == 200
    assert vault_resp.json()["total_items"] == 0


def test_cryptographic_hash_chain_linking(client: TestClient):
    headers, case_id, matches = _setup_case_with_matches(client, "chain.linking@example.com")
    assert len(matches) >= 2

    # Confirm Item 1
    client.patch(
        f"/api/v1/matches/{matches[0]['id']}",
        json={"review_status": "CONFIRMED"},
        headers=headers
    )

    # Confirm Item 2
    client.patch(
        f"/api/v1/matches/{matches[1]['id']}",
        json={"review_status": "CONFIRMED"},
        headers=headers
    )

    vault_resp = client.get(f"/api/v1/cases/{case_id}/evidence", headers=headers)
    assert vault_resp.status_code == 200
    vault = vault_resp.json()
    assert vault["total_items"] == 2
    assert vault["is_chain_valid"] is True

    item1 = vault["items"][0]
    item2 = vault["items"][1]

    assert item1["previous_evidence_hash"] == "GENESIS"
    assert item2["previous_evidence_hash"] == item1["evidence_hash"]


def test_tamper_detection_in_evidence_chain(client: TestClient, db_session: Session):
    headers, case_id, matches = _setup_case_with_matches(client, "tamper.test@example.com")
    client.patch(
        f"/api/v1/matches/{matches[0]['id']}",
        json={"review_status": "CONFIRMED"},
        headers=headers
    )

    # Vault initially valid
    vault_resp = client.get(f"/api/v1/cases/{case_id}/evidence", headers=headers)
    assert vault_resp.json()["is_chain_valid"] is True

    # Tamper with the database record directly
    db_item = db_session.query(EvidenceItem).filter(EvidenceItem.case_id == uuid.UUID(case_id)).first()
    assert db_item is not None
    db_item.source_url = "https://hacker.com/tampered-url"
    db_session.commit()

    # Re-query vault: chain integrity must detect tampering
    tampered_vault = client.get(f"/api/v1/cases/{case_id}/evidence", headers=headers).json()
    assert tampered_vault["is_chain_valid"] is False
    assert "Tampered record" in tampered_vault["verification_message"]


def test_evidence_export_endpoint(client: TestClient):
    headers, case_id, matches = _setup_case_with_matches(client, "export.test@example.com")
    client.patch(
        f"/api/v1/matches/{matches[0]['id']}",
        json={"review_status": "CONFIRMED"},
        headers=headers
    )

    export_resp = client.post(f"/api/v1/cases/{case_id}/evidence/export", headers=headers)
    assert export_resp.status_code == 200
    export_data = export_resp.json()
    assert export_data["total_evidence_items"] >= 1
    assert export_data["chain_verified"] is True
    assert len(export_data["evidence_log"]) >= 1
    first_entry = export_data["evidence_log"][0]
    assert "evidence_number" in first_entry
    assert "evidence_hash" in first_entry
