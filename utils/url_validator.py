"""
URL Validation Utility - SSRF Protection

Validates URLs before fetching to prevent Server-Side Request Forgery attacks.
Blocks requests to internal networks, cloud metadata endpoints, and non-HTTP schemes.
"""

import ipaddress
import socket
import logging
from urllib.parse import urlparse
from fastapi import HTTPException

logger = logging.getLogger(__name__)

# Known cloud metadata IP addresses
BLOCKED_IPS = {
    "169.254.169.254",  # AWS/GCP/Azure metadata
    "metadata.google.internal",  # GCP metadata hostname
    "100.100.100.200",  # Alibaba Cloud metadata
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_private_ip(ip_str: str) -> bool:
    """Check if an IP address is private, loopback, link-local, or reserved."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        )
    except ValueError:
        return False


def validate_url(url: str) -> str:
    """
    Validate a URL for safe fetching. Raises HTTPException if the URL is unsafe.

    Checks:
    - Scheme must be http or https
    - Hostname must be present
    - Hostname must not resolve to a private/internal IP
    - Hostname must not be a known cloud metadata endpoint

    Args:
        url: The URL to validate

    Returns:
        The validated URL string

    Raises:
        HTTPException: If the URL fails validation
    """
    # Parse URL
    try:
        parsed = urlparse(url)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid URL format")

    # Check scheme
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise HTTPException(
            status_code=400,
            detail=f"URL scheme '{parsed.scheme}' is not allowed. Only http and https are permitted.",
        )

    # Check hostname exists
    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(status_code=400, detail="URL must include a hostname")

    # Block known metadata hostnames
    if hostname in BLOCKED_IPS or hostname.endswith(".internal"):
        raise HTTPException(status_code=400, detail="Access to this host is not allowed")

    # Resolve hostname and check IP
    try:
        resolved_ips = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror:
        raise HTTPException(status_code=400, detail=f"Could not resolve hostname: {hostname}")

    for result in resolved_ips:
        ip_str = str(result[4][0])

        if ip_str in BLOCKED_IPS:
            raise HTTPException(status_code=400, detail="Access to this host is not allowed")

        if _is_private_ip(ip_str):
            logger.warning(f"SSRF attempt blocked: {url} resolved to private IP {ip_str}")
            raise HTTPException(
                status_code=400,
                detail="URLs pointing to internal/private networks are not allowed",
            )

    return url
