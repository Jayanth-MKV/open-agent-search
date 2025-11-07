"""
Image Search Controller
"""

import logging
from typing import Optional, List, Dict, Any
from ddgs import DDGS
from ddgs.exceptions import DDGSException, RatelimitException, TimeoutException
from fastapi import HTTPException
from models.schemas import SafeSearch, TimeLimit, ImageSize, ImageColor

logger = logging.getLogger(__name__)


def search_images(
    query: str,
    region: str = "us-en",
    safesearch: SafeSearch = SafeSearch.moderate,
    timelimit: Optional[TimeLimit] = None,
    max_results: int = 10,
    page: int = 1,
    backend: str = "auto",
    size: Optional[ImageSize] = None,
    color: Optional[ImageColor] = None,
    type_image: Optional[str] = None,
    layout: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for images with various filters.

    Args:
        query: Image search query
        region: Region code
        safesearch: Safe search level
        timelimit: Time limit
        max_results: Maximum results
        page: Page number
        backend: Search backend
        size: Image size filter
        color: Image color filter
        type_image: Image type (photo, clipart, gif, transparent, line)
        layout: Image layout (Square, Tall, Wide)

    Returns:
        List of image search results

    Raises:
        HTTPException: On various error conditions
    """
    try:
        logger.info(f"Image search: query='{query}', max_results={max_results}")

        ddgs = DDGS(timeout=10)
        results = ddgs.images(
            query=query,
            region=region,
            safesearch=safesearch.value,
            timelimit=timelimit.value if timelimit else None,
            max_results=max_results,
            page=page,
            backend=backend,
            size=size.value if size else None,
            color=color.value if color else None,
            type_image=type_image,
            layout=layout,
        )

        return results

    except RatelimitException:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except TimeoutException:
        raise HTTPException(status_code=504, detail="Request timeout")
    except DDGSException as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in image search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
