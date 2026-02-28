"""
Rate Limiting Configuration
Smart production-ready rate limits for different use cases
"""

import os
from typing import Dict


class RateLimitConfig:
    """
    Rate limit configuration for different endpoints and use cases.

    Format: "X/time_unit" where time_unit can be: second, minute, hour, day

    For larger audience usage:
    - Default: 100 requests per minute per IP
    - Search endpoints: 30 requests per minute (prevent abuse)
    - Heavy operations: 10 requests per minute (resource intensive)
    - Health/info endpoints: 200 requests per minute (monitoring friendly)
    """

    # Global default rate limit
    DEFAULT_LIMIT = "100/minute"

    # Health and informational endpoints (higher limits)
    HEALTH_LIMIT = "200/minute"
    INFO_LIMIT = "200/minute"

    # Search endpoints (moderate limits to prevent abuse)
    TEXT_SEARCH_LIMIT = "50/minute"
    IMAGE_SEARCH_LIMIT = "50/minute"
    VIDEO_SEARCH_LIMIT = "50/minute"
    NEWS_SEARCH_LIMIT = "50/minute"
    BOOK_SEARCH_LIMIT = "50/minute"

    # Heavy operations (lower limits for resource-intensive operations)
    UNIFIED_SEARCH_LIMIT = "50/minute"  # Searches across multiple sources

    # Burst limits (allow some burst traffic)
    BURST_MULTIPLIER = 2  # Allow 2x the normal rate for short bursts

    @classmethod
    def get_search_limits(cls) -> Dict[str, str]:
        """Get all search endpoint rate limits"""
        return {
            "text": cls.TEXT_SEARCH_LIMIT,
            "image": cls.IMAGE_SEARCH_LIMIT,
            "video": cls.VIDEO_SEARCH_LIMIT,
            "news": cls.NEWS_SEARCH_LIMIT,
            "book": cls.BOOK_SEARCH_LIMIT,
            "unified": cls.UNIFIED_SEARCH_LIMIT,
        }

    @classmethod
    def get_limit_description(cls) -> Dict[str, str]:
        """Get human-readable descriptions of rate limits"""
        return {
            "default": f"Default rate limit: {cls.DEFAULT_LIMIT}",
            "health": f"Health check: {cls.HEALTH_LIMIT}",
            "text_search": f"Text search: {cls.TEXT_SEARCH_LIMIT}",
            "image_search": f"Image search: {cls.IMAGE_SEARCH_LIMIT}",
            "video_search": f"Video search: {cls.VIDEO_SEARCH_LIMIT}",
            "news_search": f"News search: {cls.NEWS_SEARCH_LIMIT}",
            "book_search": f"Book search: {cls.BOOK_SEARCH_LIMIT}",
            "unified_search": f"Unified search: {cls.UNIFIED_SEARCH_LIMIT} (resource intensive)",
        }


# Environment-specific configurations
class ProductionRateLimitConfig(RateLimitConfig):
    """Production environment rate limits (more restrictive)"""

    DEFAULT_LIMIT = "60/minute"
    TEXT_SEARCH_LIMIT = "20/minute"
    IMAGE_SEARCH_LIMIT = "20/minute"
    VIDEO_SEARCH_LIMIT = "20/minute"
    NEWS_SEARCH_LIMIT = "20/minute"
    BOOK_SEARCH_LIMIT = "20/minute"
    UNIFIED_SEARCH_LIMIT = "5/minute"


class DevelopmentRateLimitConfig(RateLimitConfig):
    """Development environment rate limits (more permissive)"""

    DEFAULT_LIMIT = "200/minute"
    TEXT_SEARCH_LIMIT = "60/minute"
    IMAGE_SEARCH_LIMIT = "60/minute"
    VIDEO_SEARCH_LIMIT = "60/minute"
    NEWS_SEARCH_LIMIT = "60/minute"
    BOOK_SEARCH_LIMIT = "60/minute"
    UNIFIED_SEARCH_LIMIT = "20/minute"


# Select configuration based on environment
# You can set this via environment variable
ENVIRONMENT = os.getenv("APP_ENV", "production").lower()

if ENVIRONMENT == "development":
    rate_limit_config = DevelopmentRateLimitConfig()
elif ENVIRONMENT == "production":
    rate_limit_config = ProductionRateLimitConfig()
else:
    rate_limit_config = RateLimitConfig()
