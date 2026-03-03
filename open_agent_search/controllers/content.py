"""
Content Fetcher Controller
Fetches and extracts content from URLs
"""

import asyncio
import logging
import urllib.request
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from ddgs.http_client import HttpClient
from fastapi import HTTPException

from ..utils.url_validator import validate_url

logger = logging.getLogger(__name__)


# Maximum bytes to download in the fallback fetcher (10 MB)
_MAX_DOWNLOAD_BYTES = 10 * 1024 * 1024


def _decode_bytes_safely(raw: bytes) -> str:
    """Attempt multiple encodings to decode raw bytes into a string.

    Order matters: utf-8 first (most common), then cp1252 (Windows superset
    of latin-1 with extra printable chars), then latin-1 as a guaranteed
    fallback (maps all 256 byte values).
    """
    for encoding in ("utf-8", "cp1252"):
        try:
            return raw.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    # latin-1 never raises UnicodeDecodeError — guaranteed to succeed
    return raw.decode("latin-1")


def _fallback_fetch(url: str, timeout: int) -> tuple[str, int]:
    """Fallback fetcher using stdlib urllib when primp/DDGS client fails to decode."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "identity",  # Avoid compressed responses that may fail to decode
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        status_code = resp.getcode()
        raw_bytes = resp.read(_MAX_DOWNLOAD_BYTES)
        # Try charset from headers first
        content_type = resp.headers.get("Content-Type", "")
    charset = None
    if "charset=" in content_type:
        charset = content_type.split("charset=")[-1].strip().split(";")[0].strip()
    if charset:
        try:
            return raw_bytes.decode(charset), status_code
        except (UnicodeDecodeError, LookupError):
            pass
    return _decode_bytes_safely(raw_bytes), status_code


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
            """Network I/O done in thread pool to avoid blocking.
            Falls back to stdlib urllib if primp can't decode the response."""
            client = HttpClient(timeout=timeout, verify=True)
            response = client.request("GET", url)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")

            # Try .text first; fall back to raw bytes decoding on DecodeError
            try:
                html_text = response.text
            except Exception:
                logger.warning(f"Primary decode failed for {url!r}, trying raw bytes fallback")
                try:
                    html_text = _decode_bytes_safely(response.content)
                except Exception:
                    logger.warning(
                        f"Raw bytes fallback also failed for {url!r}, falling back to stdlib urllib"
                    )
                    raise  # will be caught by outer handler to trigger urllib fallback
            return html_text, response.status_code

        def fetch_with_urllib():
            """Fallback using stdlib urllib — no primp dependency."""
            return _fallback_fetch(url, timeout)

        # Run network I/O in thread pool to keep it non-blocking
        loop = asyncio.get_running_loop()
        try:
            html_text, status_code = await loop.run_in_executor(None, fetch_with_ddgs)
        except Exception as primary_err:
            logger.warning(
                f"DDGS client failed for {url!r}: {primary_err!r}. "
                "Retrying with stdlib urllib fallback."
            )
            html_text, status_code = await loop.run_in_executor(None, fetch_with_urllib)

        def parse_html():
            """CPU-intensive parsing done in thread pool to avoid blocking"""
            try:
                soup = BeautifulSoup(html_text, "html.parser")
            except Exception as parse_err:
                logger.warning(f"HTML parsing failed for {url!r}: {parse_err!r}")
                # Return raw text stripped of obvious tags as best-effort
                import re

                raw = re.sub(r"<[^>]+>", " ", html_text)
                raw = re.sub(r"\s+", " ", raw).strip()
                return "", "", raw

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

    except HTTPException:
        # Re-raise FastAPI exceptions (e.g. from validate_url SSRF checks) as-is
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error fetching {url}: {error_msg}")
        if "HTTP 403" in error_msg or "Forbidden" in error_msg:
            raise HTTPException(status_code=400, detail=f"Access denied (403): {url}")
        elif "HTTP 404" in error_msg:
            raise HTTPException(status_code=400, detail=f"URL not found (404): {url}")
        elif "timed out" in error_msg.lower() or "timeout" in error_msg.lower():
            raise HTTPException(status_code=408, detail=f"Request timed out: {url}")
        elif "DecodeError" in error_msg or "decode" in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail=f"Could not decode response from {url}. "
                "The page may serve binary or non-text content.",
            )
        elif "SSL" in error_msg or "certificate" in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail=f"SSL/TLS error fetching {url}: {error_msg}",
            )
        elif isinstance(
            e,
            (ConnectionError, ConnectionResetError, ConnectionRefusedError, OSError),
        ):
            raise HTTPException(
                status_code=502,
                detail=f"Connection error fetching {url}: {error_msg}",
            )
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {error_msg}")


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
