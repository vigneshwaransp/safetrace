import io
import os
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from PIL import Image, ImageOps
from app.connectors.base import PlatformConnector, CandidateMedia


class MetaConnector(PlatformConnector):
    @property
    def name(self) -> str:
        return "META"

    @property
    def display_name(self) -> str:
        return "Meta (Facebook/Instagram)"

    def is_configured(self) -> bool:
        return bool(os.getenv("META_APP_SECRET") and os.getenv("META_ACCESS_TOKEN"))

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
                    # Center square crop (typical Instagram square format)
                    w, h = pil_img.size
                    side = min(w, h)
                    left = (w - side) // 2
                    top = (h - side) // 2
                    cropped = pil_img.crop((left, top, left + side, top + side))
                    buf = io.BytesIO()
                    cropped.save(buf, format="JPEG", quality=85)
                    transformed_bytes = buf.getvalue()
                except Exception:
                    transformed_bytes = sample_bytes
            else:
                transformed_bytes = b"meta_candidate_sample_media"

            candidates.append(
                CandidateMedia(
                    platform=self.name,
                    source_url=f"https://instagram.com/p/Cmock_{idx}post99/",
                    author_handle=f"@public_share_account_{idx}",
                    post_timestamp=now - timedelta(days=2, hours=idx * 3),
                    thumbnail_url=f"https://instagram.com/mock_thumb_{idx}.jpg",
                    media_url=f"https://instagram.com/mock_media_{idx}.jpg",
                    raw_media_bytes=transformed_bytes,
                    metadata={"impressions": 350, "shares": 19}
                )
            )

        return candidates

    def fetch_url(self, url: str) -> Optional[CandidateMedia]:
        return CandidateMedia(
            platform=self.name,
            source_url=url,
            author_handle="@instagram_user",
            post_timestamp=datetime.now(timezone.utc) - timedelta(days=2),
            thumbnail_url="https://instagram.com/mock_fetch.jpg",
            media_url="https://instagram.com/mock_fetch.jpg",
            raw_media_bytes=b"meta_direct_url_media_bytes",
            metadata={"fetch_source": "meta_direct_url"}
        )
