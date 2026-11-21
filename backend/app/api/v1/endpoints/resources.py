from fastapi import APIRouter
from app.schemas.resources import OfficialResourcesResponse
from app.services.resources import get_official_resources_catalog

router = APIRouter()


@router.get("/official-channels", response_model=OfficialResourcesResponse)
def get_official_channels():
    """
    Retrieve official reporting portals, 24x7 crisis helplines (181, 1930),
    and direct platform takedown escalation links with step-by-step guidance.
    """
    return get_official_resources_catalog()
