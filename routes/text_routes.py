"""
Text Search Routes
"""

from fastapi import APIRouter, Query
from models.schemas import SafeSearch, TimeLimit, SearchResponse
from controllers.text_controller import search_text
from typing import Optional

router = APIRouter(prefix="/api/search", tags=["Text Search"])


@router.get("/text", response_model=SearchResponse)
async def text_search_route(
    q: str = Query(..., description="Search query", min_length=1),
    region: str = Query("us-en", description="Region code (e.g., us-en, uk-en, in-en)"),
    safesearch: SafeSearch = Query(
        SafeSearch.moderate, description="Safe search level"
    ),
    timelimit: Optional[TimeLimit] = Query(None, description="Time limit for results"),
    max_results: int = Query(10, ge=1, le=100, description="Maximum number of results"),
    page: int = Query(1, ge=1, description="Page number"),
    backend: str = Query(
        "auto", description="Search backend (auto, google, bing, brave, etc.)"
    ),
):
    """
    Text/Web Search Endpoint

    Search the web for text content.
    """
    results = search_text(
        query=q,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results,
        page=page,
        backend=backend,
    )

    return SearchResponse(query=q, results_count=len(results), results=results)
