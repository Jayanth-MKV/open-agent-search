# DDGS Server - Load Testing Scripts
# Quick commands to run various stress tests

Write-Host "=== DDGS Server Load Testing ===" -ForegroundColor Cyan
Write-Host ""

# Check if server is running
Write-Host "Checking if server is running on port 8000..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✓ Server is running!" -ForegroundColor Green
} catch {
    Write-Host "✗ Server is NOT running on http://localhost:8000" -ForegroundColor Red
    Write-Host "Please start the server first:" -ForegroundColor Yellow
    Write-Host "  uv run ddgs-server" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "Select a test scenario:" -ForegroundColor Cyan
Write-Host "1. Web UI (Interactive) - Best for beginners" -ForegroundColor White
Write-Host "2. Light Load Test - 10 users, 2/sec spawn rate, 1 minute" -ForegroundColor White
Write-Host "3. Normal Load Test - 50 users, 5/sec spawn rate, 2 minutes" -ForegroundColor White
Write-Host "4. Heavy Load Test - 100 users, 10/sec spawn rate, 3 minutes" -ForegroundColor White
Write-Host "5. Aggressive Rate Limit Test - 30 users, 10/sec spawn, 1 minute" -ForegroundColor White
Write-Host "6. Burst Traffic Test - 50 users, instant spawn, 30 seconds" -ForegroundColor White
Write-Host "7. Custom (Manual input)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-7)"

switch ($choice) {
    "1" {
        Write-Host "Starting Locust Web UI..." -ForegroundColor Green
        Write-Host "Open http://localhost:8089 in your browser" -ForegroundColor Yellow
        uv run locust --host=http://localhost:8000
    }
    "2" {
        Write-Host "Running Light Load Test..." -ForegroundColor Green
        uv run locust --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 1m --headless
    }
    "3" {
        Write-Host "Running Normal Load Test..." -ForegroundColor Green
        uv run locust --host=http://localhost:8000 --users 50 --spawn-rate 5 --run-time 2m --headless
    }
    "4" {
        Write-Host "Running Heavy Load Test..." -ForegroundColor Green
        uv run locust --host=http://localhost:8000 --users 100 --spawn-rate 10 --run-time 3m --headless
    }
    "5" {
        Write-Host "Running Aggressive Rate Limit Test (AggressiveUser)..." -ForegroundColor Green
        uv run locust --host=http://localhost:8000 --user AggressiveUser --users 30 --spawn-rate 10 --run-time 1m --headless
    }
    "6" {
        Write-Host "Running Burst Traffic Test (BurstUser)..." -ForegroundColor Green
        uv run locust --host=http://localhost:8000 --user BurstUser --users 50 --spawn-rate 50 --run-time 30s --headless
    }
    "7" {
        $users = Read-Host "Number of users"
        $spawnRate = Read-Host "Spawn rate (users per second)"
        $runtime = Read-Host "Run time (e.g., 1m, 30s, 2m)"
        Write-Host "Running Custom Test..." -ForegroundColor Green
        uv run locust --host=http://localhost:8000 --users $users --spawn-rate $spawnRate --run-time $runtime --headless
    }
    default {
        Write-Host "Invalid choice!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Test completed!" -ForegroundColor Green
Write-Host "Check the results above and locust_report_*.html for detailed statistics" -ForegroundColor Yellow
