"""
Test script for content fetching routes
Run this while the server is running on http://localhost:8000
"""

import json
import time

import requests

BASE_URL = "http://localhost:8000"


def test_single_url_fetch():
    """Test fetching content from a single URL"""
    print("\n" + "=" * 60)
    print("TEST 1: Fetch single URL")
    print("=" * 60)

    url = f"{BASE_URL}/api/content/fetch"
    params = {"url": "https://example.com", "timeout": 10}

    print(f"GET {url}")
    print(f"Params: {params}")

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        print(f"\n✓ Status: {response.status_code}")
        print("\n✓ Full Response:")
        print(json.dumps(data, indent=2))
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_multiple_urls_fetch():
    """Test fetching content from multiple URLs"""
    print("\n" + "=" * 60)
    print("TEST 2: Fetch multiple URLs")
    print("=" * 60)

    url = f"{BASE_URL}/api/content/fetch-multiple"
    payload = {"urls": ["https://example.com", "https://example.org"], "timeout": 10}

    print(f"POST {url}")
    print(f"Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        print(f"\n✓ Status: {response.status_code}")
        print("\n✓ Full Response:")
        print(json.dumps(data, indent=2))
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_content_trimming():
    """Test intelligent content trimming"""
    print("\n" + "=" * 60)
    print("TEST 3: Intelligent content trimming (max_length=100)")
    print("=" * 60)

    url = f"{BASE_URL}/api/content/fetch"
    params = {"url": "https://example.com", "timeout": 10, "max_length": 100}

    print(f"GET {url}")
    print(f"Params: {params}")

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        print(f"\n✓ Status: {response.status_code}")
        print("\n✓ Full Response:")
        print(json.dumps(data, indent=2))

        if "trimmed" in data:
            print(f"\n✓ Content was trimmed: {data.get('trimmed')}")
            print(f"✓ Full length: {data.get('content_length')} chars")
            print(f"✓ Returned length: {data.get('returned_length')} chars")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_invalid_url():
    """Test error handling with invalid URL"""
    print("\n" + "=" * 60)
    print("TEST 4: Error handling (invalid URL)")
    print("=" * 60)

    url = f"{BASE_URL}/api/content/fetch"
    params = {"url": "https://this-domain-does-not-exist-12345.com", "timeout": 5}

    print(f"GET {url}")
    print(f"Params: {params}")

    try:
        response = requests.get(url, params=params)
        data = response.json()

        print(f"\n✓ Status: {response.status_code}")
        print("\n✓ Full Response:")
        print(json.dumps(data, indent=2))
        if response.status_code != 200:
            print("\n✓ Error handled correctly")
            return True
        else:
            print("\n✗ Should have returned error")
            return False
    except Exception as e:
        print(f"✓ Error handled: {e}")
        return True


def test_search_and_fetch():
    """Test searching for URLs then fetching content sequentially vs parallel"""
    print("\n" + "=" * 60)
    print("TEST 5: Search + Fetch Performance")
    print("=" * 60)

    # Step 1: Search for URLs
    print("\n📍 Step 1: Searching for URLs...")
    search_url = f"{BASE_URL}/api/search/text"
    params = {"q": "python programming", "max_results": 5}

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        search_data = response.json()

        urls = [result["href"] for result in search_data["results"][:5]]
        print(f"✓ Found {len(urls)} URLs:")
        for i, url in enumerate(urls, 1):
            print(f"  {i}. {url}")

        # Step 2: Fetch content one by one (sequential)
        print("\n📍 Step 2: Fetching content SEQUENTIALLY...")
        start_sequential = time.time()

        # for i, url in enumerate(urls, 1):
        #     fetch_start = time.time()
        #     try:
        #         fetch_response = requests.get(
        #             f"{BASE_URL}/api/content/fetch",
        #             params={"url": url, "timeout": 10, "max_length": 500},
        #         )
        #         elapsed = time.time() - fetch_start
        #         if fetch_response.status_code == 200:
        #             data = fetch_response.json()
        #             print(
        #                 f"  ✓ URL {i}: {elapsed:.2f}s - {data.get('title', 'N/A')[:50]}"
        #             )
        #         else:
        #             print(f"  ✗ URL {i}: {elapsed:.2f}s - Failed")
        #     except Exception as e:
        #         elapsed = time.time() - fetch_start
        #         print(f"  ✗ URL {i}: {elapsed:.2f}s - Error: {str(e)[:50]}")

        sequential_time = time.time() - start_sequential
        # print(f"\n⏱️  Sequential Total: {sequential_time:.2f}s")

        # Step 3: Fetch content in parallel
        print("\n📍 Step 3: Fetching content in PARALLEL...")
        start_parallel = time.time()

        payload = {"urls": urls, "timeout": 10, "max_length": 500}
        fetch_response = requests.post(f"{BASE_URL}/api/content/fetch-multiple", json=payload)

        parallel_time = time.time() - start_parallel

        if fetch_response.status_code == 200:
            data = fetch_response.json()
            for i, result in enumerate(data["results"], 1):
                if "error" in result:
                    print(f"  ✗ URL {i}: Error - {result['error']}")
                else:
                    print(f"  ✓ URL {i}: {result.get('title', 'N/A')[:50]}")

            print(f"\n⏱️  Parallel Total: {parallel_time:.2f}s")

            # Performance comparison
            speedup = sequential_time / parallel_time if parallel_time > 0 else 0
            print("\n🚀 Performance Improvement:")
            print(f"   Sequential: {sequential_time:.2f}s")
            print(f"   Parallel:   {parallel_time:.2f}s")
            print(f"   Speedup:    {speedup:.2f}x faster")

            return True
        else:
            print(f"✗ Parallel fetch failed: {fetch_response.status_code}")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("CONTENT FETCHING ROUTES TEST")
    print("=" * 60)
    print("Make sure the server is running at http://localhost:8000")

    # Test server availability
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✓ Server is running (health check: {response.status_code})")
    except Exception as e:
        print(f"✗ Server not accessible: {e}")
        print("\nStart the server with: uvicorn main:app --reload")
        return

    # Run tests
    results = []
    # results.append(("Single URL fetch", test_single_url_fetch()))
    # results.append(("Multiple URLs fetch", test_multiple_urls_fetch()))
    # results.append(("Intelligent trimming", test_content_trimming()))
    # results.append(("Error handling", test_invalid_url()))
    results.append(("Search + Fetch Performance", test_search_and_fetch()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")

    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")


if __name__ == "__main__":
    main()
