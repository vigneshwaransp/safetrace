import io
from fastapi.testclient import TestClient
from tests.test_evidence import _setup_case_with_matches


def test_official_resources_endpoint(client: TestClient):
    resp = client.get("/api/v1/resources/official-channels")
    assert resp.status_code == 200
    data = resp.json()

    # Verify 1930 and 181 helplines are present
    helpline_numbers = [h["number"] for h in data["crisis_helplines"]]
    assert "1930" in helpline_numbers
    assert "181" in helpline_numbers

    # Verify official channels
    channel_ids = [c["id"] for c in data["official_channels"]]
    assert "cybercrime-gov-in" in channel_ids
    assert "stopncii-org" in channel_ids
    assert "ncmec-take-it-down" in channel_ids

    # Verify platform escalations
    platform_ids = [p["id"] for p in data["platform_escalations"]]
    assert "meta-reporting" in platform_ids
    assert "x-reporting" in platform_ids
    assert "reddit-reporting" in platform_ids


def test_create_report_and_pdf_generation(client: TestClient):
    headers, case_id, matches = _setup_case_with_matches(client, "report.gen@example.com")
    assert len(matches) >= 2

    # 1. Confirm two matches to create verified evidence
    client.patch(f"/api/v1/matches/{matches[0]['id']}", json={"review_status": "CONFIRMED"}, headers=headers)
    client.patch(f"/api/v1/matches/{matches[1]['id']}", json={"review_status": "CONFIRMED"}, headers=headers)

    vault = client.get(f"/api/v1/cases/{case_id}/evidence", headers=headers).json()
    evidence_ids = [it["id"] for it in vault["items"]]
    assert len(evidence_ids) >= 2

    # 2. Generate Consolidated Report
    report_payload = {
        "report_type": "CYBERCRIME_GOV",
        "title": "National Cybercrime Portal Complaint Package",
        "selected_evidence_ids": evidence_ids,
        "recipient_platform": "cybercrime.gov.in",
        "custom_notes": "Immediate takedown and IP preservation requested under IT Act 66E and Rule 3(2)(b)."
    }
    report_resp = client.post(f"/api/v1/cases/{case_id}/reports", json=report_payload, headers=headers)
    assert report_resp.status_code == 201
    report_data = report_resp.json()
    assert report_data["report_number"].startswith("REP-")
    assert report_data["status"] == "DRAFT"
    assert report_data["pdf_available"] is True
    assert "FORMAL NOTICE & TAKEDOWN COMPLAINT" in report_data["report_content"]

    report_id = report_data["id"]

    # 3. Download Generated ReportLab PDF
    pdf_resp = client.get(f"/api/v1/reports/{report_id}/pdf", headers=headers)
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
    assert pdf_resp.content.startswith(b"%PDF-")  # Valid PDF binary signature
    assert len(pdf_resp.content) > 1000  # Non-trivial PDF size with tables and styles


def test_report_status_progression(client: TestClient):
    headers, case_id, matches = _setup_case_with_matches(client, "report.progression@example.com")
    client.patch(f"/api/v1/matches/{matches[0]['id']}", json={"review_status": "CONFIRMED"}, headers=headers)
    vault = client.get(f"/api/v1/cases/{case_id}/evidence", headers=headers).json()
    evidence_ids = [vault["items"][0]["id"]]

    create_resp = client.post(
        f"/api/v1/cases/{case_id}/reports",
        json={
            "report_type": "PLATFORM_TAKEDOWN",
            "title": "Reddit DMCA Takedown",
            "selected_evidence_ids": evidence_ids,
            "recipient_platform": "Reddit",
        },
        headers=headers
    )
    report_id = create_resp.json()["id"]

    # Transition to SUBMITTED
    sub_resp = client.patch(
        f"/api/v1/reports/{report_id}/status",
        json={"status": "SUBMITTED", "notes": "Submitted via Reddit Report Form with Token #98234"},
        headers=headers
    )
    assert sub_resp.status_code == 200
    assert sub_resp.json()["status"] == "SUBMITTED"

    # Transition to ACKNOWLEDGED
    ack_resp = client.patch(
        f"/api/v1/reports/{report_id}/status",
        json={"status": "ACKNOWLEDGED", "notes": "Reddit Trust & Safety acknowledged receipt."},
        headers=headers
    )
    assert ack_resp.status_code == 200
    assert ack_resp.json()["status"] == "ACKNOWLEDGED"

    # Transition to REMOVED
    rem_resp = client.patch(
        f"/api/v1/reports/{report_id}/status",
        json={"status": "REMOVED", "notes": "Post confirmed deleted by moderator."},
        headers=headers
    )
    assert rem_resp.status_code == 200
    assert rem_resp.json()["status"] == "REMOVED"

    # Verify status history timeline
    report_detail = client.get(f"/api/v1/reports/{report_id}", headers=headers).json()
    history = report_detail["status_history"]
    assert len(history) >= 4  # Initial DRAFT + SUBMITTED + ACKNOWLEDGED + REMOVED


def test_unauthorized_report_access(client: TestClient):
    headers_a, case_id, matches = _setup_case_with_matches(client, "user.rep.a@example.com")
    from tests.test_cases import _get_auth_headers
    headers_b = _get_auth_headers(client, "user.rep.b@example.com")

    client.patch(f"/api/v1/matches/{matches[0]['id']}", json={"review_status": "CONFIRMED"}, headers=headers_a)
    vault = client.get(f"/api/v1/cases/{case_id}/evidence", headers=headers_a).json()
    evidence_ids = [vault["items"][0]["id"]]

    create_resp = client.post(
        f"/api/v1/cases/{case_id}/reports",
        json={
            "report_type": "CYBERCRIME_GOV",
            "title": "Confidential Package",
            "selected_evidence_ids": evidence_ids
        },
        headers=headers_a
    )
    report_id = create_resp.json()["id"]

    # User B cannot view report, download PDF, or alter status
    assert client.get(f"/api/v1/reports/{report_id}", headers=headers_b).status_code == 403
    assert client.get(f"/api/v1/reports/{report_id}/pdf", headers=headers_b).status_code == 403
    assert client.patch(f"/api/v1/reports/{report_id}/status", json={"status": "REMOVED"}, headers=headers_b).status_code == 403
