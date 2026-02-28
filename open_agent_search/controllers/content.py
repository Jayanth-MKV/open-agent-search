"""
Content Fetcher Controller
Fetches and extracts content from URLs
"""

import asyncio
import logging
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from ddgs.http_client import HttpClient
from fastapi import HTTPException

from ..utils.url_validator import validate_url

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
        # SSRF protection: validate URL before fetching
        validate_url(url)

        logger.info(f"Fetching content from: {url!r}")

        # Use DDGS HttpClient with browser impersonation for better compatibility
        # This uses primp which handles browser fingerprinting automatically
        def fetch_with_ddgs():
            """Network I/O done in thread pool to avoid blocking"""
            client = HttpClient(timeout=timeout, verify=True)
            # Use request method directly with url as positional arg
            response = client.request("GET", url)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            return response.text, response.status_code

        # Run network I/O in thread pool to keep it non-blocking
        loop = asyncio.get_running_loop()
        html_text, status_code = await loop.run_in_executor(None, fetch_with_ddgs)

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
            main_content = soup.find("main") or soup.find("article") or soup.find("body")
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

    except Exception as e:
        logger.error(f"Error fetching {url}: {str(e)}")
        if "HTTP 403" in str(e) or "Forbidden" in str(e):
            raise HTTPException(status_code=400, detail=f"Access denied (403): {url}")
        elif "HTTP 404" in str(e):
            raise HTTPException(status_code=400, detail=f"URL not found (404): {url}")
        elif "timed out" in str(e).lower():
            raise HTTPException(status_code=408, detail=f"Request timed out: {url}")
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")


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
            validate_url(url)  # SSRF protection for each URL
            return await fetch_url_content(url, timeout, max_length)
        except HTTPException as e:
            logger.error(f"Blocked or failed URL {url!r}: {e.detail}")
            return {
                "url": url,
                "error": e.detail,
                "status_code": None,
            }
        except Exception as e:
            logger.error(f"Failed to fetch {url!r}: {e!r}")
            return {
                "url": url,
                "error": str(e),
                "status_code": None,
            }

    # Fetch all URLs in parallel for better performance
    tasks = [fetch_one(url) for url in urls[:10]]  # Limit to 10 URLs
    results = await asyncio.gather(*tasks)

    return list(results)
