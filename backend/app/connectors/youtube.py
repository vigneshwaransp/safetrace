import io
import os
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from PIL import Image
from app.connectors.base import PlatformConnector, CandidateMedia


class YouTubeConnector(PlatformConnector):
    @property
    def name(self) -> str:
        return "YOUTUBE"

    @property
    def display_name(self) -> str:
        return "YouTube"

    def is_configured(self) -> bool:
        return bool(os.getenv("YOUTUBE_API_KEY"))

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
                    # Thumbnail resize 320x180 (16:9 standard YouTube thumbnail)
                    thumb = pil_img.resize((320, 180))
                    buf = io.BytesIO()
                    thumb.save(buf, format="JPEG", quality=80)
                    transformed_bytes = buf.getvalue()
                except Exception:
                    transformed_bytes = sample_bytes
            else:
                transformed_bytes = b"youtube_candidate_sample_media"

            candidates.append(
                CandidateMedia(
                    platform=self.name,
                    source_url=f"https://youtube.com/watch?v=mock_yt_{idx}abc",
                    author_handle=f"Channel_{idx}_Archive",
                    post_timestamp=now - timedelta(days=3, hours=idx),
                    thumbnail_url=f"https://i.ytimg.com/vi/mock_yt_{idx}abc/hqdefault.jpg",
                    media_url=f"https://youtube.com/watch?v=mock_yt_{idx}abc",
                    raw_media_bytes=transformed_bytes,
                    metadata={"video_id": f"mock_yt_{idx}abc", "views": 1200}
                )
            )

        return candidates

    def fetch_url(self, url: str) -> Optional[CandidateMedia]:
        return CandidateMedia(
            platform=self.name,
            source_url=url,
            author_handle="YouTubeChannel",
            post_timestamp=datetime.now(timezone.utc) - timedelta(days=3),
            thumbnail_url="https://i.ytimg.com/vi/sample/hqdefault.jpg",
            media_url=url,
            raw_media_bytes=b"youtube_direct_url_media_bytes",
            metadata={"fetch_source": "youtube_direct_url"}
        )
