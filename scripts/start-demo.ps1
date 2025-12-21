# ============================================================================
# Start Demo Script for Windows
# ============================================================================
# This script starts the Flask backend and opens the frontend in a browser.
# Run from repo root: .\scripts\start-demo.ps1
#
# Prerequisites:
# - Python virtual environment activated (.\venv\Scripts\Activate.ps1)
# - Dependencies installed (pip install -r requirements.txt)
# - .env file configured with database credentials
# ============================================================================

# Function to load .env file
function Load-EnvFile {
    param([string]$EnvPath = ".env")
    
    if (-not (Test-Path $EnvPath)) {
        Write-Host "ERROR: .env file not found at $EnvPath" -ForegroundColor Red
        Write-Host "Please copy .env.example to .env and configure your database settings." -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "Loading environment variables from $EnvPath..." -ForegroundColor Cyan
    Get-Content $EnvPath | ForEach-Object {
        $line = $_.Trim()
        # Skip empty lines and comments
        if ($line -and -not $line.StartsWith("#")) {
            $parts = $line -split "=", 2
            if ($parts.Count -eq 2) {
                $key = $parts[0].Trim()
                $value = $parts[1].Trim()
                # Remove quotes if present
                $value = $value -replace '^["'']|["'']$', ''
                Set-Item -Path "env:$key" -Value $value
                # Don't print passwords
                if ($key -like "*PASS*") {
                    Write-Host "  $key=***" -ForegroundColor DarkGray
                } else {
                    Write-Host "  $key=$value" -ForegroundColor DarkGray
                }
            }
        }
    }
}

# Change to repo root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
Set-Location $repoRoot
Write-Host "Repository root: $repoRoot" -ForegroundColor Green

# Check if venv exists
if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please create a virtual environment first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Cyan
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Cyan
    exit 1
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Install/update dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
python -m pip install -r requirements.txt --quiet --disable-pip-version-check

# Load .env
Load-EnvFile

# Get DB info for display
$dbVendor = $env:DB_VENDOR
$dbHost = $env:DB_HOST
$dbPort = $env:DB_PORT
$dbName = $env:DB_NAME

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "Starting Demo Environment" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "Database: $dbVendor at $dbHost`:$dbPort/$dbName" -ForegroundColor Yellow
Write-Host "Backend:  http://127.0.0.1:5000" -ForegroundColor Yellow
Write-Host "Frontend: file:///$repoRoot/frontend/index.html" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""

# Start Flask backend in background
Write-Host "Starting Flask backend at http://127.0.0.1:5000..." -ForegroundColor Cyan
$flaskJob = Start-Job -ScriptBlock {
    param($root)
    Set-Location $root
    & ".\venv\Scripts\python.exe" -m flask run --host 127.0.0.1 --port 5000
} -ArgumentList $repoRoot

# Wait for backend to start
Write-Host "Waiting for backend to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

# Check if Flask is running
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/health" -TimeoutSec 2 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Backend is running!" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Backend may still be starting..." -ForegroundColor Yellow
}

# Open frontend in default browser
Write-Host "Opening frontend in browser..." -ForegroundColor Cyan
$frontendPath = Join-Path $repoRoot "frontend\index.html"
Start-Process $frontendPath

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "Demo is running!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the backend server." -ForegroundColor Yellow
Write-Host "Backend Job ID: $($flaskJob.Id)" -ForegroundColor DarkGray
Write-Host ""

# Keep script running and show Flask output
try {
    while ($true) {
        Receive-Job -Job $flaskJob
        Start-Sleep -Milliseconds 500
    }
} finally {
    Write-Host ""
    Write-Host "Stopping backend server..." -ForegroundColor Yellow
    Stop-Job -Job $flaskJob
    Remove-Job -Job $flaskJob
    Write-Host "Demo stopped." -ForegroundColor Green
}
