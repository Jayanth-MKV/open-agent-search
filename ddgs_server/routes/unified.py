"""
Unified Search Routes - Search all sources at once
"""

from typing import Optional

from fastapi import APIRouter, Query, Request, Response
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..config import rate_limit_config
from ..controllers.unified import search_all
from ..models.schemas import SafeSearch, TimeLimit, UnifiedSearchResponse

router = APIRouter(prefix="/api/search", tags=["Unified Search"])

# Initialize limiter for this router
limiter = Limiter(key_func=get_remote_address)


@router.get("/all", response_model=UnifiedSearchResponse)
@limiter.limit(rate_limit_config.UNIFIED_SEARCH_LIMIT)
async def unified_search_route(
    request: Request,
    response: Response,
    q: str = Query(..., description="Search query", min_length=1),
    region: str = Query("us-en", description="Region code (e.g., us-en, uk-en, in-en)"),
    safesearch: SafeSearch = Query(SafeSearch.moderate, description="Safe search level"),
    timelimit: Optional[TimeLimit] = Query(None, description="Time limit for results"),
    max_results_per_type: int = Query(
        5, ge=1, le=50, description="Maximum number of results per search type"
    ),
    backend: str = Query("auto", description="Search backend"),
):
    """
    Unified Search Endpoint (Parallel)

    Search all sources (text, images, videos, news, books) at once in parallel.
    Returns results from all search types in a single response.
    Much faster than sequential searches!

    Rate limit: 10 requests per minute per IP (production) - Resource intensive operation
    """
    results = await search_all(
        query=q,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results_per_type=max_results_per_type,
        backend=backend,
    )

    return UnifiedSearchResponse(
        query=q,
        text_results=results["text_results"],
        image_results=results["image_results"],
        video_results=results["video_results"],
        news_results=results["news_results"],
        book_results=results["book_results"],
        total_results=results["total_results"],
    )
