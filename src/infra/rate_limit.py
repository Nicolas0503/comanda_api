from __future__ import annotations

from dataclasses import dataclass

from fastapi import Request
from slowapi import Limiter

from settings import (
    RATE_LIMIT_CRITICAL,
    RATE_LIMIT_DEFAULT,
    RATE_LIMIT_LOW,
    RATE_LIMIT_MODERATE,
    RATE_LIMIT_RESTRICTIVE,
)


@dataclass(frozen=True)
class RateLimitProfile:
    critical: str = RATE_LIMIT_CRITICAL
    restrictive: str = RATE_LIMIT_RESTRICTIVE
    moderate: str = RATE_LIMIT_MODERATE
    low: str = RATE_LIMIT_LOW
    default: str = RATE_LIMIT_DEFAULT


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()

    if request.client and request.client.host:
        return request.client.host

    return "unknown"


limits = RateLimitProfile()
limiter = Limiter(key_func=_client_ip, default_limits=[limits.default])
