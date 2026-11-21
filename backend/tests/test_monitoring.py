import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.case import Case
from app.models.report import Report
from app.models.evidence import EvidenceItem
from app.models.notification import Notification
from app.services.monitoring import check_url_liveness, run_monitoring_cycle
from app.tasks.monitoring import execute_scheduled_monitoring_cycle, check_single_url_task
from tests.test_evidence import _setup_case_with_matches


def test_url_liveness_offline_markers():
    is_live, code, msg = check_url_liveness("https://reddit.com/r/board/post_404_offline")
    assert is_live is False
    assert code == 404
    assert "offline" in msg.lower() or "removed" in msg.lower()

    is_live_ok, code_ok, _ = check_url_liveness("https://example.com/mock_media/active_test")
    assert is_live_ok is True
    assert code_ok == 200


def test_scheduled_monitoring_detects_removed_content(client: TestClient, db_session: Session):
    headers, case_id, matches = _setup_case_with_matches(client, "monitor.removed@example.com")
    # Confirm match
    client.patch(f"/api/v1/matches/{matches[0]['id']}", json={"review_status": "CONFIRMED"}, headers=headers)
    vault = client.get(f"/api/v1/cases/{case_id}/evidence", headers=headers).json()
    evidence_id = vault["items"][0]["id"]

    # Point evidence URL to an offline marker URL to simulate removal
    db_ev = db_session.query(EvidenceItem).filter(EvidenceItem.id == uuid.UUID(evidence_id)).first()
    db_ev.source_url = "https://instagram.com/p/sim_offline_takedown_success/"
    db_session.commit()

    # Create report in SUBMITTED state
    rep_resp = client.post(
        f"/api/v1/cases/{case_id}/reports",
        json={
            "report_type": "PLATFORM_TAKEDOWN",
            "title": "Takedown for Monitoring Test",
            "selected_evidence_ids": [evidence_id],
            "recipient_platform": "Instagram",
        },
        headers=headers
    )
    report_id = rep_resp.json()["id"]

    client.patch(
        f"/api/v1/reports/{report_id}/status",
        json={"status": "SUBMITTED", "notes": "Filed to Meta Trust & Safety"},
        headers=headers
    )

    # Trigger monitoring cycle via API
    mon_resp = client.post("/api/v1/monitoring/run-cycle", headers=headers)
    assert mon_resp.status_code == 200
    mon_data = mon_resp.json()
    assert mon_data["newly_removed"] >= 1

    # Verify report status transitioned automatically to REMOVED
    report_detail = client.get(f"/api/v1/reports/{report_id}", headers=headers).json()
    assert report_detail["status"] == "REMOVED"

    # Verify notification received
    notif_resp = client.get("/api/v1/notifications", headers=headers)
    assert notif_resp.status_code == 200
    notifs = notif_resp.json()
    assert notifs["unread_count"] >= 1
    assert any("Takedown Confirmed" in n["title"] for n in notifs["notifications"])


def test_scheduled_monitoring_detects_reappearance(client: TestClient, db_session: Session):
    headers, case_id, matches = _setup_case_with_matches(client, "monitor.reappear@example.com")
    client.patch(f"/api/v1/matches/{matches[0]['id']}", json={"review_status": "CONFIRMED"}, headers=headers)
    vault = client.get(f"/api/v1/cases/{case_id}/evidence", headers=headers).json()
    evidence_id = vault["items"][0]["id"]

    # Point evidence URL to active marker
    db_ev = db_session.query(EvidenceItem).filter(EvidenceItem.id == uuid.UUID(evidence_id)).first()
    db_ev.source_url = "https://reddit.com/r/public_board/reappeared_mirror/"
    db_session.commit()

    # Create report and set to REMOVED initially
    rep_resp = client.post(
        f"/api/v1/cases/{case_id}/reports",
        json={
            "report_type": "PLATFORM_TAKEDOWN",
            "title": "Reappearance Watch Case",
            "selected_evidence_ids": [evidence_id],
        },
        headers=headers
    )
    report_id = rep_resp.json()["id"]

    client.patch(
        f"/api/v1/reports/{report_id}/status",
        json={"status": "REMOVED", "notes": "Initially thought removed"},
        headers=headers
    )

    # Run monitoring cycle
    client.post("/api/v1/monitoring/run-cycle", headers=headers)

    # Verify report transitioned to REAPPEARED
    report_detail = client.get(f"/api/v1/reports/{report_id}", headers=headers).json()
    assert report_detail["status"] == "REAPPEARED"

    # Verify alert notification
    notifs = client.get("/api/v1/notifications", headers=headers).json()
    assert any("Alert: Content Re-appeared" in n["title"] for n in notifs["notifications"])


def test_user_notifications_read_management(client: TestClient):
    headers, case_id, _ = _setup_case_with_matches(client, "notif.user@example.com")

    # Fetch notifications initially
    notif_resp = client.get("/api/v1/notifications", headers=headers)
    assert notif_resp.status_code == 200
    init_data = notif_resp.json()
    
    if init_data["notifications"]:
        first_id = init_data["notifications"][0]["id"]
        # Mark single read
        patch_resp = client.patch(f"/api/v1/notifications/{first_id}/read", headers=headers)
        assert patch_resp.status_code == 200
        assert patch_resp.json()["is_read"] is True

    # Mark all read
    mark_all = client.post("/api/v1/notifications/mark-all-read", headers=headers)
    assert mark_all.status_code == 200

    after_resp = client.get("/api/v1/notifications", headers=headers).json()
    assert after_resp["unread_count"] == 0


def test_celery_task_direct_execution():
    """Verify Celery task functions execute cleanly without exceptions."""
    result = execute_scheduled_monitoring_cycle()
    assert "reports_checked" in result
    assert "timestamp" in result

    single_res = check_single_url_task("https://example.com/test_offline")
    assert single_res["is_live"] is False
