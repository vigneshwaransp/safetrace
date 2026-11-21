from typing import List, Optional
from pydantic import BaseModel


class OfficialChannelResource(BaseModel):
    id: str
    name: str
    category: str  # GOVERNMENT, HELPLINE, GLOBAL_TAKEDOWN, PLATFORM
    helpline: Optional[str] = None
    url: str
    description: str
    submission_steps: List[str]
    legal_statutes: List[str]


class HelplineResource(BaseModel):
    name: str
    number: str
    available_hours: str
    coverage: str
    description: str


class OfficialResourcesResponse(BaseModel):
    crisis_helplines: List[HelplineResource]
    official_channels: List[OfficialChannelResource]
    platform_escalations: List[OfficialChannelResource]
