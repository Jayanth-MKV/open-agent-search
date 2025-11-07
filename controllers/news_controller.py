"""
News Search Controller
"""

import logging
from typing import Optional, List, Dict, Any
from ddgs import DDGS
from ddgs.exceptions import DDGSException, RatelimitException, TimeoutException
from fastapi import HTTPException
from models.schemas import SafeSearch, TimeLimit

logger = logging.getLogger(__name__)


def search_news(
    query: str,
    region: str = "us-en",
    safesearch: SafeSearch = SafeSearch.moderate,
    timelimit: Optional[TimeLimit] = None,
    max_results: int = 10,
    page: int = 1,
    backend: str = "auto",
) -> List[Dict[str, Any]]:
    """
    Search for news articles.

    Args:
        query: News search query
        region: Region code
        safesearch: Safe search level
        timelimit: Time limit (d/w/m only)
        max_results: Maximum results
        page: Page number
        backend: Search backend (auto, duckduckgo, yahoo)

    Returns:
        List of news search results

    Raises:
        HTTPException: On various error conditions
    """
    try:
        logger.info(f"News search: query='{query}', max_results={max_results}")

        ddgs = DDGS(timeout=10)
        results = ddgs.news(
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
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout")
    except DDGSException as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in news search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
