"""
Content Fetching Routes
"""

from typing import List

from fastapi import APIRouter, Body, Query, Request, Response
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..config import rate_limit_config
from ..controllers.content import fetch_multiple_urls, fetch_url_content

router = APIRouter(prefix="/api/content", tags=["Content Fetching"])

# Initialize limiter for this router
limiter = Limiter(key_func=get_remote_address)


@router.get("/fetch")
@limiter.limit(rate_limit_config.TEXT_SEARCH_LIMIT)
async def fetch_content_route(
    request: Request,
    response: Response,
    url: str = Query(..., description="URL to fetch content from"),
    timeout: int = Query(10, ge=5, le=30, description="Request timeout in seconds"),
    max_length: int = Query(
        2000, ge=100, le=20000, description="Maximum content length (default: 2000)"
    ),
):
    """
    Fetch and extract content from a URL

    Extracts the main text content, title, and description from a webpage.
    Intelligently trims content at paragraph/sentence boundaries.
    Useful for getting article text, documentation, or any web content.
    """
    result = await fetch_url_content(url=url, timeout=timeout, max_length=max_length)
    return result


@router.post("/fetch-multiple")
@limiter.limit(rate_limit_config.TEXT_SEARCH_LIMIT)
async def fetch_multiple_route(
    request: Request,
    response: Response,
    urls: List[str] = Body(..., description="List of URLs to fetch (max 10)"),
    timeout: int = Body(10, ge=5, le=30, description="Request timeout in seconds"),
    max_length: int = Body(
        2000,
        ge=100,
        le=20000,
        description="Maximum content length per URL (default: 2000)",
    ),
):
    """
    Fetch and extract content from multiple URLs

    Processes up to 10 URLs and returns their content.
    Intelligently trims content at paragraph/sentence boundaries.
    Failed URLs will include error information instead of content.
    """
    results = await fetch_multiple_urls(urls=urls[:10], timeout=timeout, max_length=max_length)
    return {"results": results, "count": len(results)}
