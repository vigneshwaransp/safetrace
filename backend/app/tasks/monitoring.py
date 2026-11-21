from typing import Dict, Any
from app.tasks.celery_app import celery_app
from app.db.session import SessionLocal
from app.services.monitoring import run_monitoring_cycle, check_url_liveness


@celery_app.task(name="app.tasks.monitoring.run_monitoring_cycle")
def execute_scheduled_monitoring_cycle() -> Dict[str, Any]:
    """
    Celery Beat scheduled task:
    - Runs hourly URL liveness check across all active reports
    - Updates report status to REMOVED or REAPPEARED
    - Sends user notifications and compliance audit entries
    """
    db = SessionLocal()
    try:
        results = run_monitoring_cycle(db=db)
        return results
    finally:
        db.close()


@celery_app.task(name="app.tasks.monitoring.check_single_url")
def check_single_url_task(url: str) -> Dict[str, Any]:
    """Inspect liveness for an individual URL."""
    is_live, status_code, details = check_url_liveness(url)
    return {
        "url": url,
        "is_live": is_live,
        "status_code": status_code,
        "details": details,
    }
