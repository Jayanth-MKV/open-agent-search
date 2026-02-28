# API Endpoints

Open Agent Search exposes a RESTful API at `http://localhost:8000`. Interactive docs are available at [`/docs`](http://localhost:8000/docs) (Swagger UI) and [`/redoc`](http://localhost:8000/redoc) (ReDoc).

## Overview

| Endpoint                      | Method | Description                           |
| ----------------------------- | ------ | ------------------------------------- |
| `/`                           | GET    | API info & available endpoints        |
| `/health`                     | GET    | Health check                          |
| `/api/search/text`            | GET    | Web / text search                     |
| `/api/search/images`          | GET    | Image search                          |
| `/api/search/videos`          | GET    | Video search                          |
| `/api/search/news`            | GET    | News search                           |
| `/api/search/books`           | GET    | Book search                           |
| `/api/search/all`             | GET    | Unified parallel search (all sources) |
| `/api/content/fetch`          | GET    | Fetch & extract content from a URL    |
| `/api/content/fetch-multiple` | POST   | Fetch content from multiple URLs      |
| `/ai/mcp`                     | —      | MCP server endpoint                   |

---

## Text Search

`GET /api/search/text`

| Parameter      | Type   | Default    | Description                                    |
| -------------- | ------ | ---------- | ---------------------------------------------- |
| `q` (required) | string | —          | Search query                                   |
| `region`       | string | `us-en`    | Region code (`us-en`, `uk-en`, `in-en`, …)     |
| `safesearch`   | enum   | `moderate` | `on`, `moderate`, `off`                        |
| `timelimit`    | enum   | —          | `d` (day), `w` (week), `m` (month), `y` (year) |
| `max_results`  | int    | `10`       | 1–100                                          |
| `page`         | int    | `1`        | Page number                                    |
| `backend`      | string | `auto`     | Search backend                                 |

```bash
curl "http://localhost:8000/api/search/text?q=python+programming&max_results=5"
```

---

## Image Search

`GET /api/search/images`

| Parameter      | Type   | Default    | Description                                                                         |
| -------------- | ------ | ---------- | ----------------------------------------------------------------------------------- |
| `q` (required) | string | —          | Image search query                                                                  |
| `region`       | string | `us-en`    | Region code                                                                         |
| `safesearch`   | enum   | `moderate` | `on`, `moderate`, `off`                                                             |
| `timelimit`    | enum   | —          | `d`, `w`, `m`, `y`                                                                  |
| `max_results`  | int    | `10`       | 1–100                                                                               |
| `page`         | int    | `1`        | Page number                                                                         |
| `size`         | enum   | —          | `Small`, `Medium`, `Large`, `Wallpaper`                                             |
| `color`        | enum   | —          | `color`, `Monochrome`, `Red`, `Orange`, `Yellow`, `Green`, `Blue`, `Purple`, `Pink` |
| `type_image`   | string | —          | `photo`, `clipart`, `gif`, `transparent`, `line`                                    |
| `layout`       | string | —          | `Square`, `Tall`, `Wide`                                                            |

```bash
curl "http://localhost:8000/api/search/images?q=sunset&size=Large&color=Orange"
```

---

## Video Search

`GET /api/search/videos`

| Parameter        | Type   | Default    | Description                 |
| ---------------- | ------ | ---------- | --------------------------- |
| `q` (required)   | string | —          | Video search query          |
| `region`         | string | `us-en`    | Region code                 |
| `safesearch`     | enum   | `moderate` | `on`, `moderate`, `off`     |
| `timelimit`      | enum   | —          | `d`, `w`, `m`               |
| `max_results`    | int    | `10`       | 1–100                       |
| `page`           | int    | `1`        | Page number                 |
| `resolution`     | enum   | —          | `high`, `standard`          |
| `duration`       | enum   | —          | `short`, `medium`, `long`   |
| `license_videos` | string | —          | `creativeCommon`, `youtube` |

```bash
curl "http://localhost:8000/api/search/videos?q=fastapi+tutorial&resolution=high"
```

---

## News Search

`GET /api/search/news`

| Parameter      | Type   | Default    | Description                        |
| -------------- | ------ | ---------- | ---------------------------------- |
| `q` (required) | string | —          | News search query                  |
| `region`       | string | `us-en`    | Region code                        |
| `safesearch`   | enum   | `moderate` | `on`, `moderate`, `off`            |
| `timelimit`    | enum   | —          | `d` (day), `w` (week), `m` (month) |
| `max_results`  | int    | `10`       | 1–100                              |
| `page`         | int    | `1`        | Page number                        |

```bash
curl "http://localhost:8000/api/search/news?q=AI&timelimit=w&max_results=10"
```

---

## Book Search

`GET /api/search/books`

| Parameter      | Type   | Default | Description       |
| -------------- | ------ | ------- | ----------------- |
| `q` (required) | string | —       | Book search query |
| `max_results`  | int    | `10`    | 1–100             |
| `page`         | int    | `1`     | Page number       |
| `backend`      | string | `auto`  | Search backend    |

```bash
curl "http://localhost:8000/api/search/books?q=machine+learning&max_results=5"
```

---

## Unified Search

`GET /api/search/all`

Searches **all sources** (text, images, videos, news, books) in parallel and returns combined results.

| Parameter              | Type   | Default    | Description                  |
| ---------------------- | ------ | ---------- | ---------------------------- |
| `q` (required)         | string | —          | Search query                 |
| `region`               | string | `us-en`    | Region code                  |
| `safesearch`           | enum   | `moderate` | `on`, `moderate`, `off`      |
| `timelimit`            | enum   | —          | `d`, `w`, `m`, `y`           |
| `max_results_per_type` | int    | `5`        | 1–50 results per search type |

```bash
curl "http://localhost:8000/api/search/all?q=climate+change&max_results_per_type=3"
```

---

## Fetch Content

`GET /api/content/fetch`

Extract the main text content from a URL with intelligent paragraph-boundary trimming.

| Parameter        | Type   | Default | Description                                   |
| ---------------- | ------ | ------- | --------------------------------------------- |
| `url` (required) | string | —       | URL to fetch                                  |
| `timeout`        | int    | `10`    | Timeout in seconds (5–30)                     |
| `max_length`     | int    | `2000`  | Max content length in characters (100–20 000) |

```bash
curl "http://localhost:8000/api/content/fetch?url=https://example.com"
```

---

## Fetch Multiple Contents

`POST /api/content/fetch-multiple`

Fetch content from up to **10 URLs** in parallel.

**Request body** (JSON):

```json
{
  "urls": ["https://example.com", "https://example.org"],
  "timeout": 10,
  "max_length": 2000
}
```

| Field             | Type     | Default | Description                             |
| ----------------- | -------- | ------- | --------------------------------------- |
| `urls` (required) | string[] | —       | URLs to fetch (max 10)                  |
| `timeout`         | int      | `10`    | Timeout in seconds (5–30)               |
| `max_length`      | int      | `2000`  | Max content length per URL (100–20 000) |

```bash
curl -X POST "http://localhost:8000/api/content/fetch-multiple" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com", "https://example.org"]}'
```

---

## Rate Limits

All endpoints are rate-limited per IP address. Limits change based on `APP_ENV`:

| Endpoint         | Production | Development |
| ---------------- | ---------- | ----------- |
| Search endpoints | 30 req/min | 100 req/min |
| Unified search   | 10 req/min | 50 req/min  |
| Content fetch    | 30 req/min | 100 req/min |
| Health / info    | 60 req/min | 200 req/min |

Rate limit headers are included in every response (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`).

---

## Response Format

All search endpoints return:

```json
{
  "success": true,
  "query": "python programming",
  "results_count": 5,
  "results": [ ... ]
}
```

Error responses:

```json
{
  "success": false,
  "error": "Rate limit exceeded",
  "details": null
}
```
