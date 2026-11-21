import io
import os
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from PIL import Image, ImageEnhance
from app.connectors.base import PlatformConnector, CandidateMedia


class XConnector(PlatformConnector):
    @property
    def name(self) -> str:
        return "X"

    @property
    def display_name(self) -> str:
        return "X (Twitter)"

    def is_configured(self) -> bool:
        return bool(os.getenv("X_BEARER_TOKEN"))

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
                    # Adjust brightness +10% and save as Web JPEG (typical X compression)
                    bright = ImageEnhance.Brightness(pil_img).enhance(1.10)
                    buf = io.BytesIO()
                    bright.save(buf, format="JPEG", quality=80)
                    transformed_bytes = buf.getvalue()
                except Exception:
                    transformed_bytes = sample_bytes
            else:
                transformed_bytes = b"x_candidate_sample_media"

            candidates.append(
                CandidateMedia(
                    platform=self.name,
                    source_url=f"https://x.com/anon_profile_{idx}/status/178901234567890{idx}",
                    author_handle=f"@anon_leaker_{idx}",
                    post_timestamp=now - timedelta(days=idx + 1),
                    thumbnail_url=f"https://pbs.twimg.com/media/mock_thumb_{idx}?format=jpg",
                    media_url=f"https://pbs.twimg.com/media/mock_full_{idx}?format=jpg",
                    raw_media_bytes=transformed_bytes,
                    metadata={"retweets": 15, "likes": 88}
                )
            )

        return candidates

    def fetch_url(self, url: str) -> Optional[CandidateMedia]:
        return CandidateMedia(
            platform=self.name,
            source_url=url,
            author_handle="@source_handle",
            post_timestamp=datetime.now(timezone.utc) - timedelta(days=1),
            thumbnail_url="https://pbs.twimg.com/media/direct_fetch.jpg",
            media_url="https://pbs.twimg.com/media/direct_fetch.jpg",
            raw_media_bytes=b"x_direct_url_media_bytes",
            metadata={"fetch_source": "x_direct_url"}
        )
