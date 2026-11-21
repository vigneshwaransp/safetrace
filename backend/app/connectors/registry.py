from typing import Dict, List, Optional
from app.connectors.base import PlatformConnector
from app.connectors.meta import MetaConnector
from app.connectors.x_twitter import XConnector
from app.connectors.reddit import RedditConnector
from app.connectors.youtube import YouTubeConnector
from app.connectors.bluesky import BlueskyConnector
from app.connectors.web import WebUrlConnector

_CONNECTORS: Dict[str, PlatformConnector] = {
    "META": MetaConnector(),
    "X": XConnector(),
    "REDDIT": RedditConnector(),
    "YOUTUBE": YouTubeConnector(),
    "BLUESKY": BlueskyConnector(),
    "WEB": WebUrlConnector(),
}


def get_connector(platform_name: str) -> Optional[PlatformConnector]:
    """Retrieve connector instance by name (case-insensitive)."""
    return _CONNECTORS.get(platform_name.upper())


def get_all_connectors() -> List[PlatformConnector]:
    """Retrieve all available registered platform connectors."""
    return list(_CONNECTORS.values())


def get_searchable_connectors() -> List[PlatformConnector]:
    """Retrieve connectors that support automated discovery search."""
    return [c for c in _CONNECTORS.values() if c.name != "WEB"]
