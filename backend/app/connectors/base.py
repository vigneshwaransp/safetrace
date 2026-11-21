from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List


@dataclass
class CandidateMedia:
    platform: str
    source_url: str
    author_handle: Optional[str] = None
    post_timestamp: Optional[datetime] = None
    thumbnail_url: Optional[str] = None
    media_url: Optional[str] = None
    # Raw media bytes are held in-memory transiently during hashing and NEVER saved to disk
    raw_media_bytes: Optional[bytes] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class PlatformConnector(ABC):
    """Abstract Base Class for public platform discovery connectors."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Connector identifier (e.g., 'META', 'X', 'REDDIT', 'YOUTUBE', 'BLUESKY', 'WEB')."""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable display name."""
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """Return True if real API credentials are present, else sandbox mode is active."""
        pass

    @abstractmethod
    def search(
        self,
        query_terms: List[str],
        reference_images: List[Dict[str, Any]],
        limit: int = 10
    ) -> List[CandidateMedia]:
        """Search public platform sources for candidate media matching query or sample descriptors."""
        pass

    @abstractmethod
    def fetch_url(self, url: str) -> Optional[CandidateMedia]:
        """Fetch media details and transient bytes from a direct public post/media URL."""
        pass
