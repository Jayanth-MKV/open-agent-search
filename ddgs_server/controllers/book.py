"""
Book Search Controller
"""

import logging
from typing import Any, Dict, List

from ddgs import DDGS
from ddgs.exceptions import DDGSException, RatelimitException, TimeoutException
from fastapi import HTTPException

logger = logging.getLogger(__name__)


def search_books(
    query: str, max_results: int = 10, page: int = 1, backend: str = "auto"
) -> List[Dict[str, Any]]:
    """
    Search for books from Anna's Archive.

    Args:
        query: Book search query
        max_results: Maximum results
        page: Page number
        backend: Search backend

    Returns:
        List of book search results

    Raises:
        HTTPException: On various error conditions
    """
    try:
        logger.info("Book search: query=%r, max_results=%d", query, max_results)

        ddgs = DDGS(timeout=10)
        results = ddgs.books(query=query, max_results=max_results, page=page, backend=backend)

        return results

    except RatelimitException:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout")
    except DDGSException as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in book search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
