"""
Content Fetcher Controller
Fetches and extracts content from URLs
"""

import logging
from typing import List, Dict, Any
import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException
import asyncio

logger = logging.getLogger(__name__)


async def fetch_url_content(
    url: str,
    timeout: int = 10,
    max_length: int = 2000,
) -> Dict[str, Any]:
    """
    Fetch and extract content from a single URL (non-blocking async).

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        max_length: Maximum content length in characters (default: 2000)

    Returns:
        Dictionary with URL, title, content, and metadata

    Raises:
        HTTPException: On fetch errors
    """
    try:
        logger.info(f"Fetching content from: {url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        # Use async httpx client to avoid blocking
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

        # Store response data before thread pool
        html_text = response.text
        status_code = response.status_code

        def parse_html():
            """CPU-intensive parsing done in thread pool to avoid blocking"""
            soup = BeautifulSoup(html_text, "html.parser")

            # Remove script and style elements
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()

            # Extract title
            title = soup.find("title")
            title_text = title.get_text().strip() if title else ""

            # Extract main content
            main_content = (
                soup.find("main") or soup.find("article") or soup.find("body")
            )
            content = (
                main_content.get_text(separator="\n", strip=True)
                if main_content
                else soup.get_text(separator="\n", strip=True)
            )

            # Clean up content
            lines = [line.strip() for line in content.split("\n") if line.strip()]
            content = "\n".join(lines)

            # Extract meta description
            meta_desc = soup.find("meta", attrs={"name": "description"})
            description = meta_desc.get("content", "") if meta_desc else ""

            return title_text, description, content

        # Run CPU-intensive parsing in thread pool
        loop = asyncio.get_event_loop()
        title_text, description, content = await loop.run_in_executor(None, parse_html)

        # Intelligent content trimming
        full_length = len(content)
        trimmed_content = content
        is_truncated = False

        if full_length > max_length:
            # Try to cut at paragraph boundary
            trimmed_content = content[:max_length]
            last_para = trimmed_content.rfind("\n\n")
            last_sentence = trimmed_content.rfind(". ")

            if last_para > max_length * 0.7:  # If paragraph break is not too far back
                trimmed_content = content[:last_para]
            elif last_sentence > max_length * 0.8:  # Otherwise try sentence boundary
                trimmed_content = content[: last_sentence + 1]

            is_truncated = True

        return {
            "url": url,
            "title": title_text,
            "description": description,
            "content": trimmed_content,
            "content_length": full_length,
            "trimmed": is_truncated,
            "returned_length": len(trimmed_content),
            "status_code": status_code,
        }

    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching {url}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        logger.error(f"Error fetching {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing URL: {str(e)}")


async def fetch_multiple_urls(
    urls: List[str],
    timeout: int = 10,
    max_length: int = 2000,
) -> List[Dict[str, Any]]:
    """
    Fetch and extract content from multiple URLs in parallel (non-blocking).

    Args:
        urls: List of URLs to fetch
        timeout: Request timeout in seconds
        max_length: Maximum content length per URL in characters (default: 2000)

    Returns:
        List of dictionaries with URL content
    """

    async def fetch_one(url: str):
        try:
            return await fetch_url_content(url, timeout, max_length)
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {str(e)}")
            return {
                "url": url,
                "error": str(e),
                "status_code": None,
            }

    # Fetch all URLs in parallel for better performance
    tasks = [fetch_one(url) for url in urls[:10]]  # Limit to 10 URLs
    results = await asyncio.gather(*tasks)

    return list(results)
