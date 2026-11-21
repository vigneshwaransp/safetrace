import io
import os
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from PIL import Image, ImageEnhance
from app.connectors.base import PlatformConnector, CandidateMedia


class BlueskyConnector(PlatformConnector):
    @property
    def name(self) -> str:
        return "BLUESKY"

    @property
    def display_name(self) -> str:
        return "Bluesky (AT Protocol)"

    def is_configured(self) -> bool:
        return bool(os.getenv("BLUESKY_IDENTIFIER") and os.getenv("BLUESKY_PASSWORD"))

    def search(
        self,
        query_terms: List[str],
        reference_images: List[Dict[str, Any]],
        limit: int = 5
    ) -> List[CandidateMedia]:
        candidates: List[CandidateMedia] = []
        now = datetime.now(timezone.utc)

        for idx, ref in enumerate(reference_images[:limit]):
            sample_bytes = ref.get("raw_bytes")
            if sample_bytes:
                try:
                    pil_img = Image.open(io.BytesIO(sample_bytes)).convert("RGB")
                    # Contrast adjustment
                    contrast = ImageEnhance.Contrast(pil_img).enhance(1.08)
                    buf = io.BytesIO()
                    contrast.save(buf, format="JPEG", quality=85)
                    transformed_bytes = buf.getvalue()
                except Exception:
                    transformed_bytes = sample_bytes
            else:
                transformed_bytes = b"bluesky_candidate_sample_media"

            candidates.append(
                CandidateMedia(
                    platform=self.name,
                    source_url=f"https://bsky.app/profile/leaker_{idx}.bsky.social/post/3k4j5h6g{idx}",
                    author_handle=f"leaker_{idx}.bsky.social",
                    post_timestamp=now - timedelta(hours=14 * (idx + 1)),
                    thumbnail_url=f"https://cdn.bsky.app/img/thumb_{idx}.jpg",
                    media_url=f"https://cdn.bsky.app/img/full_{idx}.jpg",
                    raw_media_bytes=transformed_bytes,
                    metadata={"did": f"did:plc:mock_{idx}bluesky", "reposts": 4}
                )
            )

        return candidates

    def fetch_url(self, url: str) -> Optional[CandidateMedia]:
        return CandidateMedia(
            platform=self.name,
            source_url=url,
            author_handle="user.bsky.social",
            post_timestamp=datetime.now(timezone.utc) - timedelta(hours=8),
            thumbnail_url="https://cdn.bsky.app/img/direct_fetch.jpg",
            media_url="https://cdn.bsky.app/img/direct_fetch.jpg",
            raw_media_bytes=b"bluesky_direct_url_media_bytes",
            metadata={"fetch_source": "bluesky_direct_url"}
        )
