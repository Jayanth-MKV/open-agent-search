"""Shared pytest fixtures for DDGS Server tests."""

import pytest
from fastapi.testclient import TestClient

from open_agent_search.app import app


@pytest.fixture(scope="session")
def client():
    """Provide a FastAPI TestClient instance.

    Uses session scope because FastMCP's StreamableHTTPSessionManager
    can only be started once per instance.
    """
    with TestClient(app) as c:
        yield c
