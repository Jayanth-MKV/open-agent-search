"""
Unified Search Routes - Search all sources at once
"""

from fastapi import APIRouter, Query
from models.schemas import SafeSearch, TimeLimit, UnifiedSearchResponse
from controllers.unified_controller import search_all
from typing import Optional

router = APIRouter(prefix="/api/search", tags=["Unified Search"])


@router.get("/all", response_model=UnifiedSearchResponse)
async def unified_search_route(
    q: str = Query(..., description="Search query", min_length=1),
    region: str = Query("us-en", description="Region code (e.g., us-en, uk-en, in-en)"),
    safesearch: SafeSearch = Query(
        SafeSearch.moderate, description="Safe search level"
    ),
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
