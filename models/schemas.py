"""
Pydantic models and enums for DDGS API
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum


# Enums for validation
class SafeSearch(str, Enum):
    on = "on"
    moderate = "moderate"
    off = "off"


class TimeLimit(str, Enum):
    day = "d"
    week = "w"
    month = "m"
    year = "y"


class ImageSize(str, Enum):
    small = "Small"
    medium = "Medium"
    large = "Large"
    wallpaper = "Wallpaper"


class ImageColor(str, Enum):
    color = "color"
    monochrome = "Monochrome"
    red = "Red"
    orange = "Orange"
    yellow = "Yellow"
    green = "Green"
    blue = "Blue"
    purple = "Purple"
    pink = "Pink"


class VideoResolution(str, Enum):
    high = "high"
    standard = "standard"


class VideoDuration(str, Enum):
    short = "short"
    medium = "medium"
    long = "long"


# Response Models
class SearchResponse(BaseModel):
    success: bool = True
    query: str
    results_count: int
    results: List[Dict[str, Any]]


class UnifiedSearchResponse(BaseModel):
    success: bool = True
    query: str
    text_results: List[Dict[str, Any]]
    image_results: List[Dict[str, Any]]
    video_results: List[Dict[str, Any]]
    news_results: List[Dict[str, Any]]
    book_results: List[Dict[str, Any]]
    total_results: int


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[str] = None
