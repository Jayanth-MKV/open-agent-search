# DDGS Server - Complete Implementation

A production-ready server with DDGS metasearch integration.

---

## 📦 Project Structure

```
ddgs-server/
├── main.py                 # FastAPI app initialization and router registration
├── models/                 # Data models and schemas
│   ├── __init__.py
│   └── schemas.py         # Pydantic models and enums
├── controllers/           # Business logic layer
│   ├── __init__.py
│   ├── text_controller.py
│   ├── image_controller.py
│   ├── video_controller.py
│   ├── news_controller.py
│   ├── book_controller.py
│   └── unified_controller.py  # Searches all sources at once
├── routes/                # API route definitions
│   ├── __init__.py
│   ├── text_routes.py
│   ├── image_routes.py
│   ├── video_routes.py
│   ├── news_routes.py
│   ├── book_routes.py
│   └── unified_routes.py      # Unified search endpoint
└── public/
```



---

## 🚀 Quick Start

### 1. Installation

```bash
# Create project directory
mkdir ddgs-server
cd ddgs-server

# Install dependencies
pip install uvicorn ddgs pydantic python-multipart
```

### 2. Run the Server

```bash
# Save the main.py file from the generated code
# Then run:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000

---

## 🔌 API Endpoints

### Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/api/search/text` | GET | Web/text search |
| `/api/search/images` | GET | Image search |
| `/api/search/videos` | GET | Video search |
| `/api/search/news` | GET | News search |
| `/api/search/books` | GET | Book search |

---

## 📝 Endpoint Details

### 1. Text/Web Search

**Endpoint**: `GET /api/search/text`

**Parameters**:
- `q` (required): Search query
- `region` (optional): Region code (default: us-en)
- `safesearch` (optional): on/moderate/off (default: moderate)
- `timelimit` (optional): d/w/m/y
- `max_results` (optional): 1-100 (default: 10)
- `page` (optional): Page number (default: 1)
- `backend` (optional): Search backend (default: auto)

**Example**:
```bash
curl "http://localhost:8000/api/search/text?q=python%20programming&max_results=5"
```

**Response**:
```json
{
  "success": true,
  "query": "python programming",
  "results_count": 5,
  "results": [
    {
      "title": "Python Programming Language",
      "href": "https://www.python.org/",
      "body": "Official Python website..."
    }
  ]
}
```

---

### 2. Image Search

**Endpoint**: `GET /api/search/images`

**Additional Parameters**:
- `size`: Small/Medium/Large/Wallpaper
- `color`: color/Monochrome/Red/Orange/Yellow/Green/Blue/Purple/Pink
- `type_image`: photo/clipart/gif/transparent/line
- `layout`: Square/Tall/Wide

**Example**:
```bash
curl "http://localhost:8000/api/search/images?q=butterfly&size=Large&color=color"
```

---

### 3. Video Search

**Endpoint**: `GET /api/search/videos`

**Additional Parameters**:
- `resolution`: high/standard
- `duration`: short/medium/long
- `license_videos`: creativeCommon/youtube

**Example**:
```bash
curl "http://localhost:8000/api/search/videos?q=tutorial&resolution=high&duration=medium"
```

---

### 4. News Search

**Endpoint**: `GET /api/search/news`

**Parameters**:
- Same as text search
- `timelimit` limited to: d/w/m

**Example**:
```bash
curl "http://localhost:8000/api/search/news?q=technology&timelimit=w&max_results=20"
```

---

### 5. Book Search

**Endpoint**: `GET /api/search/books`

**Parameters**:
- `q` (required): Search query
- `max_results` (optional): 1-100 (default: 10)
- `page` (optional): Page number

**Example**:
```bash
curl "http://localhost:8000/api/search/books?q=machine%20learning&max_results=15"
```

---

## 🐍 Python Client Usage

```python
import requests

# Text search
response = requests.get(
    "http://localhost:8000/api/search/text",
    params={
        "q":  tutorial",
        "region": "us-en",
        "max_results": 10
    }
)

data = response.json()
print(f"Found {data['results_count']} results")

for result in data['results']:
    print(f"- {result['title']}: {result['href']}")
```

---

## 🌐 JavaScript/Fetch Usage

```javascript
// Image search
fetch('http://localhost:8000/api/search/images?q=nature&size=Large&max_results=20')
  .then(response => response.json())
  .then(data => {
    console.log(`Found ${data.results_count} images`);
    data.results.forEach(img => {
      console.log(img.title, img.image);
    });
  });
```

---

## 🧪 Testing with cURL

### Text Search
```bash
curl -X GET "http://localhost:8000/api/search/text?q=python&max_results=5" \
  -H "accept: application/json"
```

### Image Search with Filters
```bash
curl -X GET "http://localhost:8000/api/search/images?q=sunset&size=Large&color=Orange" \
  -H "accept: application/json"
```

### News Search (Last Week)
```bash
curl -X GET "http://localhost:8000/api/search/news?q=AI&timelimit=w&max_results=10" \
  -H "accept: application/json"
```

---

## 🐳 Docker Deployment

### Using Docker

```bash
# Build image
docker build -t ddgs-api .

# Run container
docker run -p 8000:8000 ddgs-api
```

### Using Docker Compose

```bash
# Start service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```bash
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=info
DDGS_TIMEOUT=10
DDGS_PROXY=  # Optional proxy
```

### Using Proxy

Modify the DDGS initialization in `main.py`:

```python
ddgs = DDGS(
    proxy="socks5h://127.0.0.1:9150",  # Tor browser
    timeout=10
)
```

---

## 🔒 Security Features

1. **Input Validation**: Pydantic models validate all inputs
2. **Rate Limit Handling**: Proper HTTP 429 responses
3. **Error Handling**: Comprehensive exception handling
4. **Type Safety**: Full type hints throughout
5. **Logging**: Request logging for monitoring

---

## 📊 Response Format

### Success Response

```json
{
  "success": true,
  "query": "search term",
  "results_count": 10,
  "results": [...]
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error message",
  "details": "Additional error details"
}
```

---

## 🚦 HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 429 | Rate Limit Exceeded |
| 504 | Gateway Timeout |
| 500 | Internal Server Error |

---

## 🛠️ Advanced Features

### CORS Configuration

Add CORS middleware for cross-origin requests:

```python
from.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting

Install and add rate limiting:

```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/search/text")
@limiter.limit("30/minute")
async def search_text(...):
    ...
```

---

## 📈 Production Tips

1. **Use multiple workers**:
   ```bash
   uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
   ```

2. **Set up reverse proxy** (Nginx example):
   ```nginx
   location / {
       proxy_pass http://localhost:8000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
   }
   ```

3. **Enable HTTPS** using Certbot/Let's Encrypt

4. **Monitor with logging**:
   - Use structured logging
   - Send logs to monitoring service

5. **Use environment-based configuration**

---

## 📚 Full Code Files

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  ddgs-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=info
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## 🔍 Testing the Server


### Manual Testing

```bash
# Health check
curl http://localhost:8000/health

# API root
curl http://localhost:8000/

# Text search
curl "http://localhost:8000/api/search/text?q=test&max_results=3"
```

---

## 🎯 Features Summary

✅ **5 Complete Search Endpoints**
- Text/Web Search
- Image Search with filters
- Video Search with filters
- News Search
- Book Search

✅ **Production Ready**
- Auto-generated API documentation
- Input validation with Pydantic
- Comprehensive error handling
- Logging and monitoring
- Docker support

✅ **Developer Friendly**
- Type hints throughout
- Clear endpoint documentation
- Example client code
- Easy to extend

---

## 📝 License

MIT License

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📧 Support

For issues:
- *Server**: Check the documentation at http://localhost:8000/docs
- **DDGS Library**: Visit https://pypi.org/project/ddgs/

---

## 🎉 Ready to Use!

Your DDGS server is now complete with:
- Full implementation in `main.py`
- Test client in `test_client.py`
- Docker configuration
- Comprehensive documentation
- Production-ready features

Start the server and visit http://localhost:8000/docs to explore the interactive API documentation!
