"""
Locust Load Testing Configuration for Open Agent Search
Stress test your rate-limited API with realistic usage patterns

Run with:
    locust --host=http://localhost:8000
    # Then open http://localhost:8089 in your browser

Or headless mode:
    locust --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 1m --headless
"""

import random

from locust import HttpUser, TaskSet, between, task


class SearchBehavior(TaskSet):
    """
    Realistic user behavior: performs various types of searches
    """

    # Common search queries for testing
    search_queries = [
        "python programming",
        "artificial intelligence",
        "climate change",
        "latest news",
        "technology trends",
        "machine learning",
        "web development",
        "data science",
        "cybersecurity",
        "renewable energy",
    ]

    regions = ["us-en", "uk-en", "in-en"]

    @task(10)
    def text_search(self):
        """Text search - most common operation (weight: 10)"""
        query = random.choice(self.search_queries)
        self.client.get(
            "/api/search/text",
            params={
                "q": query,
                "region": random.choice(self.regions),
                "max_results": random.randint(5, 20),
            },
            name="/api/search/text",
        )

    @task(5)
    def image_search(self):
        """Image search (weight: 5)"""
        query = random.choice(self.search_queries)
        self.client.get(
            "/api/search/images",
            params={
                "q": query,
                "region": random.choice(self.regions),
                "max_results": random.randint(5, 15),
            },
            name="/api/search/images",
        )

    @task(5)
    def news_search(self):
        """News search (weight: 5)"""
        query = random.choice(self.search_queries)
        self.client.get(
            "/api/search/news",
            params={
                "q": query,
                "region": random.choice(self.regions),
                "max_results": random.randint(5, 15),
            },
            name="/api/search/news",
        )

    @task(3)
    def video_search(self):
        """Video search (weight: 3)"""
        query = random.choice(self.search_queries)
        self.client.get(
            "/api/search/videos",
            params={
                "q": query,
                "region": random.choice(self.regions),
                "max_results": random.randint(5, 10),
            },
            name="/api/search/videos",
        )

    @task(2)
    def book_search(self):
        """Book search (weight: 2)"""
        query = random.choice(self.search_queries)
        self.client.get(
            "/api/search/books",
            params={
                "q": query,
                "max_results": random.randint(5, 10),
            },
            name="/api/search/books",
        )

    @task(1)
    def unified_search(self):
        """Unified search - most resource intensive (weight: 1)"""
        query = random.choice(self.search_queries)
        self.client.get(
            "/api/search/all",
            params={
                "q": query,
                "region": random.choice(self.regions),
                "max_results_per_type": 5,
            },
            name="/api/search/all (unified)",
        )

    @task(20)
    def health_check(self):
        """Health check - most frequent (weight: 20)"""
        self.client.get("/health", name="/health")

    @task(5)
    def root_endpoint(self):
        """Root endpoint info (weight: 5)"""
        self.client.get("/", name="/")


class RateLimitTestUser(HttpUser):
    """
    Simulates a normal user with realistic think time
    Good for testing rate limits under normal load
    """

    tasks = [SearchBehavior]
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    def on_start(self):
        """Called when a user starts"""
        self.client.get("/health")


class AggressiveUser(HttpUser):
    """
    Aggressive user that quickly hits rate limits
    Use this to test rate limiting behavior
    """

    tasks = [SearchBehavior]
    wait_time = between(0.1, 0.5)  # Very short wait time

    def on_start(self):
        """Called when a user starts"""
        self.client.get("/health")


class BurstUser(HttpUser):
    """
    User that sends burst traffic
    Simulates sudden spikes in usage
    """

    tasks = [SearchBehavior]
    wait_time = between(0, 0.1)  # Almost no wait time

    def on_start(self):
        """Called when a user starts"""
        self.client.get("/health")


# Default user class (you can specify with --user flag)
# Example: locust --user RateLimitTestUser
# Or: locust --user AggressiveUser
# Or: locust --user BurstUser
