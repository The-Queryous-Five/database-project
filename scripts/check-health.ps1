# Database Health Check Script for Windows
# Tests database connectivity and basic queries.

# Function to load .env file
function Load-EnvFile {
    param([string]$EnvPath = ".env")
    
    if (-not (Test-Path $EnvPath)) {
        Write-Host "ERROR: .env file not found at $EnvPath" -ForegroundColor Red
        exit 1
    }
    
    Get-Content $EnvPath | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#")) {
            $parts = $line -split "=", 2
            if ($parts.Count -eq 2) {
                $key = $parts[0].Trim()
                $value = $parts[1].Trim()
                $value = $value -replace '^["'']|["'']$', ''
                Set-Item -Path "env:$key" -Value $value
            }
        }
    }
}

# Change to repo root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
Set-Location $repoRoot

# Load environment variables
Load-EnvFile

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "Database Health Check" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "Database: $env:DB_VENDOR at $env:DB_HOST`:$env:DB_PORT/$env:DB_NAME" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""

# Check Python and test script
$testScript = "tools\test_db_connection.py"
$pythonPath = ".\venv\Scripts\python.exe"

if (-not (Test-Path $pythonPath)) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    exit 1
}

# Run the test
Write-Host "Running database connection test..." -ForegroundColor Cyan

if (Test-Path $testScript) {
    & $pythonPath -m tools.test_db_connection
    $exitCode = $LASTEXITCODE
} else {
    Write-Host "WARNING: tools\test_db_connection.py not found, using basic test" -ForegroundColor Yellow
    
    # Basic connection test
    $exitCode = 1
    try {
        & $pythonPath -c "import os; from app.db.db import get_conn; conn=get_conn(); conn.close(); print('[OK] Connection successful'); exit(0)"
        $exitCode = $LASTEXITCODE
    } catch {
        Write-Host "[ERROR] Connection test failed" -ForegroundColor Red
        $exitCode = 1
    }
}

Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "============================================================================" -ForegroundColor Green
    Write-Host "[OK] HEALTH CHECK PASSED" -ForegroundColor Green
    Write-Host "============================================================================" -ForegroundColor Green
    Write-Host "Database is ready for demo!" -ForegroundColor Yellow
    Write-Host ""
    exit 0
} else {
    Write-Host "============================================================================" -ForegroundColor Red
    Write-Host "[ERROR] HEALTH CHECK FAILED" -ForegroundColor Red
    Write-Host "============================================================================" -ForegroundColor Red
    Write-Host "Please check your database connection settings." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
