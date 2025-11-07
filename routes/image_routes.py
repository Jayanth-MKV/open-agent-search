"""
Image Search Routes
"""

from fastapi import APIRouter, Query, Request, Response
from models.schemas import SafeSearch, TimeLimit, ImageSize, ImageColor, SearchResponse
from controllers.image_controller import search_images
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from config import rate_limit_config
from utils import run_in_threadpool

router = APIRouter(prefix="/api/search", tags=["Image Search"])

# Initialize limiter for this router
limiter = Limiter(key_func=get_remote_address)


@router.get("/images", response_model=SearchResponse)
@limiter.limit(rate_limit_config.IMAGE_SEARCH_LIMIT)
async def image_search_route(
    request: Request,
    response: Response,
    q: str = Query(..., description="Image search query", min_length=1),
    region: str = Query("us-en", description="Region code"),
    safesearch: SafeSearch = Query(
        SafeSearch.moderate, description="Safe search level"
    ),
    timelimit: Optional[TimeLimit] = Query(None, description="Time limit"),
    max_results: int = Query(10, ge=1, le=100, description="Maximum results"),
    page: int = Query(1, ge=1, description="Page number"),
    backend: str = Query("auto", description="Search backend"),
    size: Optional[ImageSize] = Query(None, description="Image size filter"),
    color: Optional[ImageColor] = Query(None, description="Image color filter"),
    type_image: Optional[str] = Query(
        None, description="Image type (photo, clipart, gif, transparent, line)"
    ),
    layout: Optional[str] = Query(
        None, description="Image layout (Square, Tall, Wide)"
    ),
):
    """
    Image Search Endpoint

    Search for images with various filters.
    Rate limit: 30 requests per minute per IP (production)
    """
    # Run blocking DDGS call in thread pool
    results = await run_in_threadpool(
        search_images,
        query=q,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results,
        page=page,
        backend=backend,
        size=size,
        color=color,
        type_image=type_image,
        layout=layout,
    )

    return SearchResponse(query=q, results_count=len(results), results=results)
