import io
import os
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from PIL import Image, ImageEnhance
from app.connectors.base import PlatformConnector, CandidateMedia


class RedditConnector(PlatformConnector):
    @property
    def name(self) -> str:
        return "REDDIT"

    @property
    def display_name(self) -> str:
        return "Reddit"

    def is_configured(self) -> bool:
        return bool(os.getenv("REDDIT_CLIENT_ID") and os.getenv("REDDIT_CLIENT_SECRET"))

    def search(
        self,
        query_terms: List[str],
        reference_images: List[Dict[str, Any]],
        limit: int = 5
    ) -> List[CandidateMedia]:
        candidates: List[CandidateMedia] = []

        # If live credentials exist, we would invoke the Reddit API here
        # Sandbox / Mock implementation generates realistic transformed candidates for the demo
        now = datetime.now(timezone.utc)
        for idx, ref in enumerate(reference_images[:limit]):
            # 1. High-similarity candidate: slightly resized & compressed copy
            sample_bytes = ref.get("raw_bytes")
            if sample_bytes:
                try:
                    pil_img = Image.open(io.BytesIO(sample_bytes)).convert("RGB")
                    resized = pil_img.resize((int(pil_img.width * 0.85), int(pil_img.height * 0.85)))
                    buf = io.BytesIO()
                    resized.save(buf, format="JPEG", quality=75)
                    transformed_bytes = buf.getvalue()
                except Exception:
                    transformed_bytes = sample_bytes
            else:
                transformed_bytes = b"reddit_candidate_sample_media"

            candidates.append(
                CandidateMedia(
                    platform=self.name,
                    source_url=f"https://reddit.com/r/public_board/comments/leak_{idx}987/image_post",
                    author_handle="u/repost_bot_44",
                    post_timestamp=now - timedelta(hours=idx * 6 + 2),
                    thumbnail_url=f"https://preview.redd.it/mock_thumb_{idx}.jpg",
                    media_url=f"https://i.redd.it/mock_media_{idx}.jpg",
                    raw_media_bytes=transformed_bytes,
                    metadata={"subreddit": "public_board", "upvotes": 42 + idx * 10, "comments": 8}
                )
            )

        return candidates

    def fetch_url(self, url: str) -> Optional[CandidateMedia]:
        return CandidateMedia(
            platform=self.name,
            source_url=url,
            author_handle="u/source_author",
            post_timestamp=datetime.now(timezone.utc) - timedelta(hours=5),
            thumbnail_url="https://preview.redd.it/sample_fetch.jpg",
            media_url="https://i.redd.it/sample_fetch.jpg",
            raw_media_bytes=b"reddit_direct_url_media_bytes",
            metadata={"fetch_source": "reddit_direct_url"}
        )
