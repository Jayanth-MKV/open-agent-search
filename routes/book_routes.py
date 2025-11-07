"""
Book Search Routes
"""

from fastapi import APIRouter, Query
from models.schemas import SearchResponse
from controllers.book_controller import search_books

router = APIRouter(prefix="/api/search", tags=["Book Search"])


@router.get("/books", response_model=SearchResponse)
async def book_search_route(
    q: str = Query(..., description="Book search query", min_length=1),
    max_results: int = Query(10, ge=1, le=100, description="Maximum results"),
    page: int = Query(1, ge=1, description="Page number"),
    backend: str = Query("auto", description="Search backend"),
):
    """
    Book Search Endpoint

    Search for books from Anna's Archive.
    """
    results = search_books(query=q, max_results=max_results, page=page, backend=backend)

    return SearchResponse(query=q, results_count=len(results), results=results)
