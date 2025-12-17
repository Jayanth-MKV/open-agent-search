"""
DDGS FastAPI Server - main.py
A complete REST API server using the DDGS library for metasearch functionality.

Install dependencies:
pip install fastapi uvicorn ddgs pydantic slowapi

Run the server:
uvicorn main:app --reload --host 0.0.0.0 --port 8000

API Documentation:
http://localhost:8000/docs
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Import routes
from routes.text_routes import router as text_router
from routes.image_routes import router as image_router
from routes.video_routes import router as video_router
from routes.news_routes import router as news_router
from routes.book_routes import router as book_router
from routes.unified_routes import router as unified_router
from routes.content_routes import router as content_router

# Import models for exception handling
from models.schemas import ErrorResponse

# Import rate limit configuration
from config import rate_limit_config

# Import MCP server
from mcp_server import mcp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,  # Rate limit by IP address
    default_limits=[rate_limit_config.DEFAULT_LIMIT],  # Global default
    storage_uri="memory://",  # In-memory storage (use Redis for production clusters)
    headers_enabled=True,  # Add rate limit info to response headers
)

# Create MCP ASGI app
mcp_app = mcp.http_app("/mcp")

# Initialize FastAPI app with MCP lifespan
app = FastAPI(
    title="DDGS Metasearch API",
    description="A comprehensive metasearch API powered by DDGS library with smart rate limiting",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=mcp_app.lifespan,
)

# Add rate limiter to app state
app.state.limiter = limiter


# Register rate limit exceeded handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded errors"""
    return _rate_limit_exceeded_handler(request, exc)


# Register routers
app.include_router(text_router)
app.include_router(image_router)
app.include_router(video_router)
app.include_router(news_router)
app.include_router(book_router)
app.include_router(unified_router)
app.include_router(content_router)

# Mount MCP server
app.mount("/ai", mcp_app)


# Root endpoint
@app.get("/")
@limiter.limit(rate_limit_config.INFO_LIMIT)
async def root(request: Request, response: Response):
    """Root endpoint with API information"""
    return {
        "message": "DDGS Metasearch API",
        "version": "1.0.0",
        "rate_limits": rate_limit_config.get_limit_description(),
        "endpoints": {
            "text_search": "/api/search/text",
            "image_search": "/api/search/images",
            "video_search": "/api/search/videos",
            "news_search": "/api/search/news",
            "book_search": "/api/search/books",
            "unified_search": "/api/search/all",
            "fetch_content": "/api/content/fetch",
            "fetch_multiple": "/api/content/fetch-multiple",
            "mcp_server": "/mcp",
            "documentation": "/docs",
        },
    }


# Health check endpoint
@app.get("/health")
@limiter.limit(rate_limit_config.HEALTH_LIMIT)
async def health_check(request: Request, response: Response):
    """Health check endpoint"""
    return {"status": "healthy", "service": "DDGS API"}


# Exception handlers
from fastapi import HTTPException


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code, content=ErrorResponse(error=exc.detail).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(error="Internal server error", details=str(exc)).dict(),
    )


if __name__ == "__main__":
    import uvicorn

    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
