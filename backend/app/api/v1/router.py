from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    auth,
    cases,
    discovery,
    evidence,
    reports,
    resources,
    notifications,
    monitoring,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(cases.router, prefix="/cases", tags=["Cases & Uploads"])
api_router.include_router(discovery.router, tags=["Discovery & Matches"])
api_router.include_router(evidence.router, tags=["Evidence Vault & Review"])
api_router.include_router(reports.router, tags=["Bulk Reporting & PDF"])
api_router.include_router(resources.router, prefix="/resources", tags=["Official Resources & Helplines"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["Monitoring & Compliance"])
