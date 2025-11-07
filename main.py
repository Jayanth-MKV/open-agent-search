"""
DDGS FastAPI Server - main.py
A complete REST API server using the DDGS library for metasearch functionality.

Install dependencies:
pip install fastapi uvicorn ddgs pydantic

Run the server:
uvicorn main:app --reload --host 0.0.0.0 --port 8000

API Documentation:
http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging

# Import routes
from routes.text_routes import router as text_router
from routes.image_routes import router as image_router
from routes.video_routes import router as video_router
from routes.news_routes import router as news_router
from routes.book_routes import router as book_router
from routes.unified_routes import router as unified_router

# Import models for exception handling
from models.schemas import ErrorResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="DDGS Metasearch API",
    description="A comprehensive metasearch API powered by DDGS library",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register routers
app.include_router(text_router)
app.include_router(image_router)
app.include_router(video_router)
app.include_router(news_router)
app.include_router(book_router)
app.include_router(unified_router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "DDGS Metasearch API",
        "version": "1.0.0",
        "endpoints": {
            "text_search": "/api/search/text",
            "image_search": "/api/search/images",
            "video_search": "/api/search/videos",
            "news_search": "/api/search/news",
            "book_search": "/api/search/books",
            "unified_search": "/api/search/all",
            "documentation": "/docs",
        },
    }


# Health check endpoint
@app.get("/health")
async def health_check():
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

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
