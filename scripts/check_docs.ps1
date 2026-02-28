#!/usr/bin/env pwsh
# check_docs.ps1 — validates that MkDocs build produces correctly structured pages.
# Run: uv run mkdocs build && .\scripts\check_docs.ps1

$errors = 0

function Check-File {
    param([string]$path, [string]$label)

    if (-not (Test-Path $path)) {
        Write-Host "SKIP  $label — file not found at $path"
        return
    }

    $content = [System.IO.File]::ReadAllText($path)

    # 1. No raw emoji shortcodes should remain unrendered
    $rawEmoji = [regex]::Matches($content, ':material-[a-z-]+:|:simple-[a-z-]+:|:octicons-[a-z0-9-]+:|:fontawesome-[a-z-]+:')
    if ($rawEmoji.Count -gt 0) {
        foreach ($m in $rawEmoji) {
            Write-Host "FAIL  $label — unrendered emoji shortcode: $($m.Value)"
            $script:errors++
        }
    } else {
        Write-Host "OK    $label — no raw emoji shortcodes"
    }

    # 2. Grid cards content must NOT break out of <li> elements
    #    Bad pattern: </li></ul><hr>  (description escapes the <li>)
    if ($content -match '</li>\s*</ul>\s*<hr') {
        Write-Host "FAIL  $label — grid cards layout broken (content escaping <li>)"
        $script:errors++
    } else {
        Write-Host "OK    $label — grid cards layout correct"
    }
}

Write-Host ""
Write-Host "=== Docs HTML Validation ==="
Write-Host ""

Check-File "site/index.html"          "Home page"
Check-File "site/mcp/index.html"      "MCP index"
Check-File "site/getting-started/installation/index.html" "Installation"
Check-File "site/api/endpoints/index.html"                "API endpoints"

Write-Host ""
if ($errors -gt 0) {
    Write-Host "RESULT  $errors error(s) found. Run 'uv run mkdocs build' to regenerate." -ForegroundColor Red
    exit 1
} else {
    Write-Host "RESULT  All checks passed." -ForegroundColor Green
    exit 0
}
