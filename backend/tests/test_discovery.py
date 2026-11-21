import io
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.connectors.registry import get_connector, get_all_connectors
from tests.test_cases import _get_auth_headers
from tests.test_fingerprint import _generate_test_image


def test_connector_registry():
    connectors = get_all_connectors()
    assert len(connectors) >= 6
    names = [c.name for c in connectors]
    assert "META" in names
    assert "X" in names
    assert "REDDIT" in names
    assert "YOUTUBE" in names
    assert "BLUESKY" in names
    assert "WEB" in names

    reddit = get_connector("reddit")
    assert reddit is not None
    assert reddit.display_name == "Reddit"


def test_discovery_job_execution_and_ranking(client: TestClient):
    headers = _get_auth_headers(client, "discovery.user@example.com")

    # 1. Create a case
    case_resp = client.post("/api/v1/cases", json={"title": "Discovery Test Case", "retain_encrypted_originals": True}, headers=headers)
    assert case_resp.status_code == 201
    case_id = case_resp.json()["id"]

    # 2. Upload an image
    img_bytes = _generate_test_image((300, 300))
    upload_resp = client.post(
        f"/api/v1/cases/{case_id}/images",
        files={"file": ("test.jpg", io.BytesIO(img_bytes), "image/jpeg")},
        headers=headers
    )
    assert upload_resp.status_code == 201

    # 3. Trigger Discovery Job
    discover_resp = client.post(
        f"/api/v1/cases/{case_id}/discover",
        json={"platforms": ["REDDIT", "X", "META", "YOUTUBE", "BLUESKY"]},
        headers=headers
    )
    assert discover_resp.status_code == 202
    job_data = discover_resp.json()
    assert job_data["status"] == "COMPLETED"
    assert job_data["results_count"] > 0
    assert "REDDIT" in job_data["platforms_searched"]

    # 4. Fetch Ranked Matches
    matches_resp = client.get(f"/api/v1/cases/{case_id}/matches", headers=headers)
    assert matches_resp.status_code == 200
    matches = matches_resp.json()
    assert len(matches) > 0

    # Assert matches are ranked by similarity_score in descending order
    scores = [m["similarity_score"] for m in matches]
    assert scores == sorted(scores, reverse=True)

    # Assert first match has reasons and confidence band
    top_match = matches[0]
    assert len(top_match["match_reasons"]) > 0
    assert top_match["confidence_band"] in ["HIGH", "MEDIUM", "LOW"]
    assert top_match["review_status"] == "UNREVIEWED"
    assert top_match["source_url"].startswith("http")


def test_discovery_on_empty_case_fails(client: TestClient):
    headers = _get_auth_headers(client, "emptycase@example.com")
    case_resp = client.post("/api/v1/cases", json={"title": "Empty Case"}, headers=headers)
    case_id = case_resp.json()["id"]

    # Discovery without images must return 400 Bad Request
    discover_resp = client.post(f"/api/v1/cases/{case_id}/discover", json={}, headers=headers)
    assert discover_resp.status_code == 400
    assert "no uploaded fingerprints" in discover_resp.json()["detail"].lower()


def test_manual_url_submission(client: TestClient):
    headers = _get_auth_headers(client, "manualurl@example.com")
    case_resp = client.post("/api/v1/cases", json={"title": "Manual URL Case"}, headers=headers)
    case_id = case_resp.json()["id"]

    img_bytes = _generate_test_image((250, 250))
    client.post(
        f"/api/v1/cases/{case_id}/images",
        files={"file": ("target.jpg", io.BytesIO(img_bytes), "image/jpeg")},
        headers=headers
    )

    url_resp = client.post(
        f"/api/v1/cases/{case_id}/urls",
        json={"url": "https://example.com/reported-post/123"},
        headers=headers
    )
    assert url_resp.status_code == 201
    matches = url_resp.json()
    assert len(matches) >= 1
    assert matches[0]["platform"] == "WEB"
    assert matches[0]["source_url"] == "https://example.com/reported-post/123"


def test_discovery_unauthorized_isolation(client: TestClient):
    headers_a = _get_auth_headers(client, "user_a@example.com")
    headers_b = _get_auth_headers(client, "user_b@example.com")

    # User A creates case
    case_resp = client.post("/api/v1/cases", json={"title": "User A Private Case"}, headers=headers_a)
    case_id = case_resp.json()["id"]

    # User B tries to trigger discovery or view matches on User A's case
    disc_resp = client.post(f"/api/v1/cases/{case_id}/discover", json={}, headers=headers_b)
    assert disc_resp.status_code == 403

    matches_resp = client.get(f"/api/v1/cases/{case_id}/matches", headers=headers_b)
    assert matches_resp.status_code == 403
