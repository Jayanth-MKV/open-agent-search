"""
Text/Web Search Controller
"""

import logging
from typing import Optional, List, Dict, Any
from ddgs import DDGS
from ddgs.exceptions import DDGSException, RatelimitException, TimeoutException
from fastapi import HTTPException
from models.schemas import SafeSearch, TimeLimit

logger = logging.getLogger(__name__)


def search_text(
    query: str,
    region: str = "us-en",
    safesearch: SafeSearch = SafeSearch.moderate,
    timelimit: Optional[TimeLimit] = None,
    max_results: int = 10,
    page: int = 1,
    backend: str = "auto",
) -> List[Dict[str, Any]]:
    """
    Search the web for text content.

    Args:
        query: Search query string
        region: Region code (e.g., us-en, uk-en)
        safesearch: Safe search level
        timelimit: Time limit for results
        max_results: Maximum number of results
        page: Page number
        backend: Search backend

    Returns:
        List of search results

    Raises:
        HTTPException: On various error conditions
    """
    try:
        logger.info("Text search: query=%r, max_results=%d", query, max_results)

        ddgs = DDGS(timeout=10)
        results = ddgs.text(
            query=query,
            region=region,
            safesearch=safesearch.value,
            timelimit=timelimit.value if timelimit else None,
            max_results=max_results,
            page=page,
            backend=backend,
        )

        return results

    except RatelimitException:
        raise HTTPException(
            status_code=429, detail="Rate limit exceeded. Please try again later."
        )
    except TimeoutException:
        raise HTTPException(
            status_code=504, detail="Request timeout. Please try again."
        )
    except DDGSException as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in text search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
