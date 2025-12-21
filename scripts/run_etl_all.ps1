# ============================================================================
# Run All ETL Scripts for Windows
# ============================================================================
# Runs all ETL scripts in the correct dependency order.
# Run from repo root: .\scripts\run_etl_all.ps1
#
# Prerequisites:
# - Python virtual environment activated
# - Database created and DDL applied
# - .env file configured
# ============================================================================

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

# Force production mode (no dry run)
$env:DRY_RUN = "0"

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "Running ETL Pipeline" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "Database:    $env:DB_VENDOR at $env:DB_HOST`:$env:DB_PORT/$env:DB_NAME" -ForegroundColor Yellow
Write-Host "ETL Scripts: db\etl\" -ForegroundColor Yellow
Write-Host "DRY_RUN:     $env:DRY_RUN (0 = actual load)" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""

# Check if venv is activated
$pythonPath = ".\venv\Scripts\python.exe"
if (-not (Test-Path $pythonPath)) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please activate venv: .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    exit 1
}

# ETL scripts in dependency order
$etlScripts = @(
    "load_categories.py",
    "load_geo_zip.py",
    "load_products.py",
    "load_customers.py",
    "load_sellers.py",
    "load_orders.py",
    "load_order_items.py",
    "load_payments.py",
    "load_reviews.py"
)

$etlDir = "db\etl"
$successCount = 0
$totalCount = $etlScripts.Count

foreach ($script in $etlScripts) {
    $scriptPath = Join-Path $etlDir $script
    
    if (-not (Test-Path $scriptPath)) {
        Write-Host "WARNING: $script not found, skipping..." -ForegroundColor Yellow
        continue
    }
    
    Write-Host "[$($successCount + 1)/$totalCount] Running $script..." -ForegroundColor Cyan
    
    try {
        & $pythonPath $scriptPath
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ $script completed successfully" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "  ✗ $script failed (exit code: $LASTEXITCODE)" -ForegroundColor Red
            Write-Host ""
            Write-Host "ETL pipeline stopped due to error." -ForegroundColor Yellow
            Write-Host "Fix the issue and run this script again." -ForegroundColor Yellow
            exit 1
        }
    } catch {
        Write-Host "  ✗ Error running $script`: $_" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
}

Write-Host "============================================================================" -ForegroundColor Green
Write-Host "✓ ETL Pipeline Complete!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "Successfully loaded $successCount/$totalCount datasets" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next step: .\scripts\check-health.ps1" -ForegroundColor Cyan
