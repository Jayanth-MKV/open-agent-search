"""
Book Search Routes
"""

from fastapi import APIRouter, Query, Request, Response
from models.schemas import SearchResponse
from controllers.book_controller import search_books
from slowapi import Limiter
from slowapi.util import get_remote_address
from config import rate_limit_config
from utils import run_in_threadpool

router = APIRouter(prefix="/api/search", tags=["Book Search"])

# Initialize limiter for this router
limiter = Limiter(key_func=get_remote_address)


@router.get("/books", response_model=SearchResponse)
@limiter.limit(rate_limit_config.BOOK_SEARCH_LIMIT)
async def book_search_route(
    request: Request,
    response: Response,
    q: str = Query(..., description="Book search query", min_length=1),
    max_results: int = Query(10, ge=1, le=100, description="Maximum results"),
    page: int = Query(1, ge=1, description="Page number"),
    backend: str = Query("auto", description="Search backend"),
):
    """
    Book Search Endpoint

    Search for books from Anna's Archive.
    Rate limit: 30 requests per minute per IP (production)
    """
    # Run blocking DDGS call in thread pool
    results = await run_in_threadpool(
        search_books, query=q, max_results=max_results, page=page, backend=backend
    )

    return SearchResponse(query=q, results_count=len(results), results=results)
