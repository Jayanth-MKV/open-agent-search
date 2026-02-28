"""Smoke tests for the DDGS Server API."""


def test_root(client):
    """Root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "DDGS Metasearch API"
    assert "endpoints" in data


def test_health(client):
    """Health check returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_text_search_missing_query(client):
    """Text search without query returns 422."""
    response = client.get("/api/search/text")
    assert response.status_code == 422


def test_image_search_missing_query(client):
    """Image search without query returns 422."""
    response = client.get("/api/search/images")
    assert response.status_code == 422


def test_content_fetch_missing_url(client):
    """Content fetch without url returns 422."""
    response = client.get("/api/content/fetch")
    assert response.status_code == 422
