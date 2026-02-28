"""
Video Search Controller
"""

import logging
from typing import Optional, List, Dict, Any
from ddgs import DDGS
from ddgs.exceptions import DDGSException, RatelimitException, TimeoutException
from fastapi import HTTPException
from models.schemas import SafeSearch, TimeLimit, VideoResolution, VideoDuration

logger = logging.getLogger(__name__)


def search_videos(
    query: str,
    region: str = "us-en",
    safesearch: SafeSearch = SafeSearch.moderate,
    timelimit: Optional[TimeLimit] = None,
    max_results: int = 10,
    page: int = 1,
    backend: str = "auto",
    resolution: Optional[VideoResolution] = None,
    duration: Optional[VideoDuration] = None,
    license_videos: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for videos with filters.

    Args:
        query: Video search query
        region: Region code
        safesearch: Safe search level
        timelimit: Time limit (d/w/m only)
        max_results: Maximum results
        page: Page number
        backend: Search backend
        resolution: Video resolution (high/standard)
        duration: Video duration (short/medium/long)
        license_videos: Video license (creativeCommon, youtube)

    Returns:
        List of video search results

    Raises:
        HTTPException: On various error conditions
    """
    try:
        logger.info("Video search: query=%r, max_results=%d", query, max_results)

        ddgs = DDGS(timeout=10)
        results = ddgs.videos(
            query=query,
            region=region,
            safesearch=safesearch.value,
            timelimit=timelimit.value if timelimit else None,
            max_results=max_results,
            page=page,
            backend=backend,
            resolution=resolution.value if resolution else None,
            duration=duration.value if duration else None,
            license_videos=license_videos,
        )

        return results

    except RatelimitException:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout")
    except DDGSException as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in video search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
