import time
from collections import defaultdict
from typing import Dict, List, Tuple
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.config import settings


class InMemoryRateLimiter:
    """
    Sliding window in-memory rate limiter per IP address.
    Tracks timestamps of requests within a moving window.
    """

    def __init__(self, requests_per_minute: int = 120):
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
        self.hits: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> Tuple[bool, int]:
        now = time.time()
        cutoff = now - self.window_seconds

        # Prune old hits outside sliding window
        self.hits[client_ip] = [ts for ts in self.hits[client_ip] if ts > cutoff]

        current_count = len(self.hits[client_ip])
        if current_count >= self.requests_per_minute:
            retry_after = int(self.hits[client_ip][0] + self.window_seconds - now) + 1
            return False, max(1, retry_after)

        self.hits[client_ip].append(now)
        return True, 0


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 120):
        super().__init__(app)
        self.limiter = InMemoryRateLimiter(requests_per_minute)

    async def dispatch(self, request: Request, call_next):
        # Allow open healthchecks / docs / openapi schema without rate limits
        path = request.url.path
        if path in ["/", f"{settings.API_V1_STR}/docs", f"{settings.API_V1_STR}/openapi.json", f"{settings.API_V1_STR}/redoc"]:
            return await call_next(request)

        # Get client IP
        forwarded = request.headers.get("X-Forwarded-For")
        client_ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "127.0.0.1")

        allowed, retry_after = self.limiter.is_allowed(client_ip)
        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded. Please wait before retrying."},
                headers={"Retry-After": str(retry_after)},
            )

        return await call_next(request)
