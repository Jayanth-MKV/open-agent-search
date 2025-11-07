"""
Unified Search Controller - searches all sources at once in parallel
"""

import logging
import asyncio
from typing import Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from models.schemas import SafeSearch, TimeLimit
from controllers.text_controller import search_text
from controllers.image_controller import search_images
from controllers.video_controller import search_videos
from controllers.news_controller import search_news
from controllers.book_controller import search_books

logger = logging.getLogger(__name__)


async def search_all(
    query: str,
    region: str = "us-en",
    safesearch: SafeSearch = SafeSearch.moderate,
    timelimit: Optional[TimeLimit] = None,
    max_results_per_type: int = 5,
    backend: str = "auto",
) -> Dict[str, Any]:
    """
    Search all sources (text, images, videos, news, books) at once in parallel.

    Args:
        query: Search query string
        region: Region code
        safesearch: Safe search level
        timelimit: Time limit for results
        max_results_per_type: Maximum number of results per search type
        backend: Search backend

    Returns:
        Dictionary containing results from all search types
    """
    logger.info(
        f"Unified search (parallel): query='{query}', max_results_per_type={max_results_per_type}"
    )

    # Create a thread pool executor for running blocking I/O operations
    loop = asyncio.get_event_loop()

    # Define async wrapper functions for each search
    async def get_text_results():
        try:
            return await loop.run_in_executor(
                None,
                lambda: search_text(
                    query=query,
                    region=region,
                    safesearch=safesearch,
                    timelimit=timelimit,
                    max_results=max_results_per_type,
                    backend=backend,
                ),
            )
        except Exception as e:
            logger.warning(f"Text search failed: {str(e)}")
            return []

    async def get_image_results():
        try:
            return await loop.run_in_executor(
                None,
                lambda: search_images(
                    query=query,
                    region=region,
                    safesearch=safesearch,
                    timelimit=timelimit,
                    max_results=max_results_per_type,
                    backend=backend,
                ),
            )
        except Exception as e:
            logger.warning(f"Image search failed: {str(e)}")
            return []

    async def get_video_results():
        try:
            return await loop.run_in_executor(
                None,
                lambda: search_videos(
                    query=query,
                    region=region,
                    safesearch=safesearch,
                    timelimit=timelimit,
                    max_results=max_results_per_type,
                    backend=backend,
                ),
            )
        except Exception as e:
            logger.warning(f"Video search failed: {str(e)}")
            return []

    async def get_news_results():
        try:
            return await loop.run_in_executor(
                None,
                lambda: search_news(
                    query=query,
                    region=region,
                    safesearch=safesearch,
                    timelimit=timelimit,
                    max_results=max_results_per_type,
                    backend=backend,
                ),
            )
        except Exception as e:
            logger.warning(f"News search failed: {str(e)}")
            return []

    async def get_book_results():
        try:
            return await loop.run_in_executor(
                None,
                lambda: search_books(
                    query=query, max_results=max_results_per_type, backend=backend
                ),
            )
        except Exception as e:
            logger.warning(f"Book search failed: {str(e)}")
            return []

    # Run all searches in parallel
    text_results, image_results, video_results, news_results, book_results = (
        await asyncio.gather(
            get_text_results(),
            get_image_results(),
            get_video_results(),
            get_news_results(),
            get_book_results(),
        )
    )

    total_results = (
        len(text_results)
        + len(image_results)
        + len(video_results)
        + len(news_results)
        + len(book_results)
    )

    return {
        "text_results": text_results,
        "image_results": image_results,
        "video_results": video_results,
        "news_results": news_results,
        "book_results": book_results,
        "total_results": total_results,
    }
