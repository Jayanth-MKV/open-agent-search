"""
Video Search Routes
"""

from typing import Optional

from fastapi import APIRouter, Query, Request, Response
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..config import rate_limit_config
from ..controllers.video import search_videos
from ..models.schemas import (
    SafeSearch,
    SearchResponse,
    TimeLimit,
    VideoDuration,
    VideoResolution,
)
from ..utils import run_in_threadpool

router = APIRouter(prefix="/api/search", tags=["Video Search"])

# Initialize limiter for this router
limiter = Limiter(key_func=get_remote_address)


@router.get("/videos", response_model=SearchResponse)
@limiter.limit(rate_limit_config.VIDEO_SEARCH_LIMIT)
async def video_search_route(
    request: Request,
    response: Response,
    q: str = Query(..., description="Video search query", min_length=1),
    region: str = Query("us-en", description="Region code"),
    safesearch: SafeSearch = Query(SafeSearch.moderate, description="Safe search level"),
    timelimit: Optional[TimeLimit] = Query(None, description="Time limit (d/w/m only)"),
    max_results: int = Query(10, ge=1, le=100, description="Maximum results"),
    page: int = Query(1, ge=1, description="Page number"),
    backend: str = Query("auto", description="Search backend"),
    resolution: Optional[VideoResolution] = Query(
        None, description="Video resolution (high/standard)"
    ),
    duration: Optional[VideoDuration] = Query(
        None, description="Video duration (short/medium/long)"
    ),
    license_videos: Optional[str] = Query(
        None, description="Video license (creativeCommon, youtube)"
    ),
):
    """
    Video Search Endpoint

    Search for videos with filters.
    Rate limit: 30 requests per minute per IP (production)
    """
    # Run blocking DDGS call in thread pool
    results = await run_in_threadpool(
        search_videos,
        query=q,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results,
        page=page,
        backend=backend,
        resolution=resolution,
        duration=duration,
        license_videos=license_videos,
    )

    return SearchResponse(query=q, results_count=len(results), results=results)
