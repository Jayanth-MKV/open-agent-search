"""MCP Server for Open Agent Search — provides LLM-friendly search tools via FastMCP."""

from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from .controllers.book import search_books as controller_search_books
from .controllers.content import fetch_multiple_urls, fetch_url_content
from .controllers.image import search_images as controller_search_images
from .controllers.news import search_news as controller_search_news
from .controllers.text import search_text as controller_search_text
from .controllers.unified import search_all
from .controllers.video import search_videos as controller_search_videos
from .models.schemas import (
    ImageColor,
    ImageSize,
    SafeSearch,
    TimeLimit,
    VideoDuration,
    VideoResolution,
)

# Create MCP server
mcp = FastMCP("Open Agent Search Tools", stateless_http=True)


@mcp.tool()
def search_web(
    query: str,
    region: str = "us-en",
    max_results: int = 10,
    safesearch: str = "moderate",
) -> List[Dict[str, Any]]:
    """
    Search the web for text content.

    Args:
        query: Search query string (required)
        region: Region code like 'us-en', 'uk-en', 'in-en' (default: 'us-en')
        max_results: Maximum number of results, 1-100 (default: 10)
        safesearch: Safe search level: 'on', 'moderate', 'off' (default: 'moderate')

    Returns:
        List of search results with title, body, and url
    """
    return controller_search_text(
        query=query,
        region=region,
        safesearch=SafeSearch(safesearch),
        max_results=min(max_results, 100),
        page=1,
        backend="auto",
    )


@mcp.tool()
def search_images(
    query: str,
    region: str = "us-en",
    max_results: int = 10,
    safesearch: str = "moderate",
    size: Optional[str] = None,
    color: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for images.

    Args:
        query: Image search query (required)
        region: Region code (default: 'us-en')
        max_results: Maximum results, 1-100 (default: 10)
        safesearch: Safe search: 'on', 'moderate', 'off' (default: 'moderate')
        size: Image size filter: 'small', 'medium', 'large', 'wallpaper'
        color: Color filter: 'color', 'monochrome', 'red', 'orange', 'yellow',
            'green', 'blue', 'purple', 'pink', 'brown', 'black', 'gray', 'teal', 'white'

    Returns:
        List of images with title, image url, thumbnail, source, and more
    """
    return controller_search_images(
        query=query,
        region=region,
        safesearch=SafeSearch(safesearch),
        max_results=min(max_results, 100),
        size=ImageSize(size) if size else None,
        color=ImageColor(color) if color else None,
        page=1,
    )


@mcp.tool()
def search_videos(
    query: str,
    region: str = "us-en",
    max_results: int = 10,
    safesearch: str = "moderate",
    resolution: Optional[str] = None,
    duration: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for videos.

    Args:
        query: Video search query (required)
        region: Region code (default: 'us-en')
        max_results: Maximum results, 1-100 (default: 10)
        safesearch: Safe search: 'on', 'moderate', 'off' (default: 'moderate')
        resolution: Video resolution: 'high', 'standard'
        duration: Video duration: 'short', 'medium', 'long'

    Returns:
        List of videos with title, description, url, duration, and more
    """
    return controller_search_videos(
        query=query,
        region=region,
        safesearch=SafeSearch(safesearch),
        max_results=min(max_results, 100),
        resolution=VideoResolution(resolution) if resolution else None,
        duration=VideoDuration(duration) if duration else None,
        page=1,
    )


@mcp.tool()
def search_news(
    query: str,
    region: str = "us-en",
    max_results: int = 10,
    safesearch: str = "moderate",
    timelimit: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for news articles.

    Args:
        query: News search query (required)
        region: Region code (default: 'us-en')
        max_results: Maximum results, 1-100 (default: 10)
        safesearch: Safe search: 'on', 'moderate', 'off' (default: 'moderate')
        timelimit: Time limit: 'd' (day), 'w' (week), 'm' (month)

    Returns:
        List of news articles with title, body, url, date, and source
    """
    return controller_search_news(
        query=query,
        region=region,
        safesearch=SafeSearch(safesearch),
        timelimit=TimeLimit(timelimit) if timelimit else None,
        max_results=min(max_results, 100),
        page=1,
    )


@mcp.tool()
def search_books(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search for books.

    Args:
        query: Book search query (required)
        max_results: Maximum results, 1-100 (default: 10)

    Returns:
        List of books with title, authors, and links
    """
    return controller_search_books(
        query=query, max_results=min(max_results, 100), page=1, backend="auto"
    )


@mcp.tool()
async def search_everything(
    query: str,
    region: str = "us-en",
    max_results_per_type: int = 5,
    safesearch: str = "moderate",
) -> Dict[str, Any]:
    """
    Search all sources at once (text, images, videos, news, books).

    Args:
        query: Search query (required)
        region: Region code (default: 'us-en')
        max_results_per_type: Results per category, 1-20 (default: 5)
        safesearch: Safe search: 'on', 'moderate', 'off' (default: 'moderate')

    Returns:
        Dictionary with results from all search types
    """
    return await search_all(
        query=query,
        region=region,
        safesearch=SafeSearch(safesearch),
        max_results_per_type=min(max_results_per_type, 20),
    )


@mcp.tool()
async def fetch_content(url: str, timeout: int = 10, max_length: int = 2000) -> Dict[str, Any]:
    """
    Fetch and extract content from a URL with intelligent trimming (non-blocking).

    Args:
        url: URL to fetch content from (required)
        timeout: Request timeout in seconds, 5-30 (default: 10)
        max_length: Maximum content length in characters, 100-20000 (default: 2000)

    Returns:
        Extracted content with title, description, and intelligently trimmed text
    """
    return await fetch_url_content(
        url=url,
        timeout=min(max(timeout, 5), 30),
        max_length=min(max(max_length, 100), 20000),
    )


@mcp.tool()
async def fetch_multiple_contents(
    urls: List[str], timeout: int = 10, max_length: int = 2000
) -> Dict[str, Any]:
    """
    Fetch and extract content from multiple URLs in parallel (max 10, non-blocking).

    Args:
        urls: List of URLs to fetch (required, max 10)
        timeout: Request timeout in seconds, 5-30 (default: 10)
        max_length: Maximum content length per URL, 100-20000 (default: 2000)

    Returns:
        Dictionary with list of extracted content from each URL
    """
    results = await fetch_multiple_urls(
        urls=urls[:10],
        timeout=min(max(timeout, 5), 30),
        max_length=min(max(max_length, 100), 20000),
    )
    return {"results": results, "count": len(results)}


def main():
    """CLI entry point: run the MCP server over stdio (for Claude Desktop / Cursor)."""
    mcp.run(transport="stdio")
