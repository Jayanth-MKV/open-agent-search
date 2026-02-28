"""
Text Search Routes
"""

from typing import Optional

from fastapi import APIRouter, Query, Request, Response
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..config import rate_limit_config
from ..controllers.text import search_text
from ..models.schemas import SafeSearch, SearchResponse, TimeLimit
from ..utils import run_in_threadpool

router = APIRouter(prefix="/api/search", tags=["Text Search"])

# Initialize limiter for this router
limiter = Limiter(key_func=get_remote_address)


@router.get("/text", response_model=SearchResponse)
@limiter.limit(rate_limit_config.TEXT_SEARCH_LIMIT)
async def text_search_route(
    request: Request,
    response: Response,
    q: str = Query(..., description="Search query", min_length=1),
    region: str = Query("us-en", description="Region code (e.g., us-en, uk-en, in-en)"),
    safesearch: SafeSearch = Query(SafeSearch.moderate, description="Safe search level"),
    timelimit: Optional[TimeLimit] = Query(None, description="Time limit for results"),
    max_results: int = Query(10, ge=1, le=100, description="Maximum number of results"),
    page: int = Query(1, ge=1, description="Page number"),
    backend: str = Query("auto", description="Search backend (auto, google, bing, brave, etc.)"),
):
    """
    Text/Web Search Endpoint

    Search the web for text content.
    Rate limit: 30 requests per minute per IP (production)
    """
    # Run blocking DDGS call in thread pool
    results = await run_in_threadpool(
        search_text,
        query=q,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results,
        page=page,
        backend=backend,
    )

    return SearchResponse(query=q, results_count=len(results), results=results)
