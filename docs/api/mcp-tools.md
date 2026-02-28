# MCP Tools Reference

Both **stdio** and **HTTP** transports expose the same 8 tools. This page documents every tool, its parameters, and example return values.

---

## search_web

Search the web for text content.

| Parameter    | Type   | Default    | Description                                     |
| ------------ | ------ | ---------- | ----------------------------------------------- |
| `query`      | string | (required) | Search query                                    |
| `region`     | string | `us-en`    | Region code (`us-en`, `uk-en`, `in-en`, …)      |
| `max_results`| int    | `10`       | 1–100                                           |
| `safesearch` | string | `moderate` | `on`, `moderate`, `off`                         |

**Returns:** list of `{ title, body, url }`

---

## search_images

Search for images with optional size and colour filters.

| Parameter    | Type   | Default    | Description                                                                        |
| ------------ | ------ | ---------- | ---------------------------------------------------------------------------------- |
| `query`      | string | (required) | Image search query                                                                 |
| `region`     | string | `us-en`    | Region code                                                                        |
| `max_results`| int    | `10`       | 1–100                                                                              |
| `safesearch` | string | `moderate` | `on`, `moderate`, `off`                                                            |
| `size`       | string | —          | `small`, `medium`, `large`, `wallpaper`                                            |
| `color`      | string | —          | `color`, `monochrome`, `red`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink` |

**Returns:** list of `{ title, image, thumbnail, url, source, … }`

---

## search_videos

Search for videos with optional resolution and duration filters.

| Parameter    | Type   | Default    | Description                    |
| ------------ | ------ | ---------- | ------------------------------ |
| `query`      | string | (required) | Video search query             |
| `region`     | string | `us-en`    | Region code                    |
| `max_results`| int    | `10`       | 1–100                          |
| `safesearch` | string | `moderate` | `on`, `moderate`, `off`        |
| `resolution` | string | —          | `high`, `standard`             |
| `duration`   | string | —          | `short`, `medium`, `long`      |

**Returns:** list of `{ title, description, url, duration, … }`

---

## search_news

Search for news articles with optional time filter.

| Parameter    | Type   | Default    | Description                             |
| ------------ | ------ | ---------- | --------------------------------------- |
| `query`      | string | (required) | News search query                       |
| `region`     | string | `us-en`    | Region code                             |
| `max_results`| int    | `10`       | 1–100                                   |
| `safesearch` | string | `moderate` | `on`, `moderate`, `off`                 |
| `timelimit`  | string | —          | `d` (day), `w` (week), `m` (month)      |

**Returns:** list of `{ title, body, url, date, source }`

---

## search_books

Search for books.

| Parameter    | Type   | Default    | Description        |
| ------------ | ------ | ---------- | ------------------ |
| `query`      | string | (required) | Book search query  |
| `max_results`| int    | `10`       | 1–100              |

**Returns:** list of `{ title, authors, … }`

---

## search_everything

Search **all sources** (text, images, videos, news, books) in a single call. Results are fetched in parallel.

| Parameter            | Type   | Default    | Description                         |
| -------------------- | ------ | ---------- | ----------------------------------- |
| `query`              | string | (required) | Search query                        |
| `region`             | string | `us-en`    | Region code                         |
| `max_results_per_type`| int   | `5`        | 1–20 results per category           |
| `safesearch`         | string | `moderate` | `on`, `moderate`, `off`             |

**Returns:** `{ text_results, image_results, video_results, news_results, book_results }`

---

## fetch_content

Fetch and extract the main content from a single URL. Content is trimmed at natural paragraph/sentence boundaries.

| Parameter    | Type   | Default    | Description                                     |
| ------------ | ------ | ---------- | ----------------------------------------------- |
| `url`        | string | (required) | URL to fetch                                    |
| `timeout`    | int    | `10`       | Timeout in seconds (5–30)                       |
| `max_length` | int    | `2000`     | Max content length in characters (100–20 000)   |

**Returns:** `{ title, description, content, url }`

---

## fetch_multiple_contents

Fetch and extract content from **multiple URLs** in parallel (max 10).

| Parameter    | Type     | Default    | Description                                   |
| ------------ | -------- | ---------- | --------------------------------------------- |
| `urls`       | string[] | (required) | URLs to fetch (max 10)                        |
| `timeout`    | int      | `10`       | Timeout in seconds (5–30)                     |
| `max_length` | int      | `2000`     | Max content length per URL (100–20 000)       |

**Returns:** `{ results: [ { title, description, content, url }, … ], count }`
