# Database Health Check Script for Windows
# Tests database connectivity and basic queries
# Run from repo root: .\scripts\check-health.ps1

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

# Check if official test tool exists
$testScript = "tools\test_db_connection.py"
$pythonPath = ".\venv\Scripts\python.exe"

if (-not (Test-Path $pythonPath)) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    exit 1
}

if (Test-Path $testScript) {
    # Use the official test tool
    Write-Host "Running database connection test..." -ForegroundColor Cyan
    
    & $pythonPath -m tools.test_db_connection
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "============================================================================" -ForegroundColor Green
        Write-Host "SUCCESS: HEALTH CHECK PASSED" -ForegroundColor Green
        Write-Host "============================================================================" -ForegroundColor Green
        Write-Host "Database is ready for demo!" -ForegroundColor Yellow
        Write-Host ""
        exit 0
    } else {
        Write-Host ""
        Write-Host "============================================================================" -ForegroundColor Red
        Write-Host "FAILED: HEALTH CHECK FAILED" -ForegroundColor Red
        Write-Host "============================================================================" -ForegroundColor Red
        Write-Host "Please check your database connection settings." -ForegroundColor Yellow
        Write-Host ""
        exit 1
    }
} else {
    # Fallback: basic connection test
    Write-Host "WARNING: $testScript not found, using basic test..." -ForegroundColor Yellow
    Write-Host ""
    
    & $pythonPath -c "import os, sys; db_vendor = os.getenv('DB_VENDOR'); print(f'Testing {db_vendor} connection...'); import mysql.connector if db_vendor == 'mysql' else __import__('psycopg'); conn = mysql.connector.connect(host=os.getenv('DB_HOST'), port=int(os.getenv('DB_PORT', 3306)), user=os.getenv('DB_USER'), password=os.getenv('DB_PASS'), database=os.getenv('DB_NAME')) if db_vendor == 'mysql' else __import__('psycopg').connect(host=os.getenv('DB_HOST'), port=int(os.getenv('DB_PORT', 5432)), user=os.getenv('DB_USER'), password=os.getenv('DB_PASS'), dbname=os.getenv('DB_NAME')); cursor = conn.cursor(); cursor.execute('SELECT 1'); result = cursor.fetchone(); cursor.close(); conn.close(); print('SUCCESS: Connection test passed!'); sys.exit(0)"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "============================================================================" -ForegroundColor Green
        Write-Host "SUCCESS: HEALTH CHECK PASSED" -ForegroundColor Green
        Write-Host "============================================================================" -ForegroundColor Green
        exit 0
    } else {
        Write-Host ""
        Write-Host "============================================================================" -ForegroundColor Red
        Write-Host "FAILED: HEALTH CHECK FAILED" -ForegroundColor Red
        Write-Host "============================================================================" -ForegroundColor Red
        exit 1
    }
}
