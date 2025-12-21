# Run Minimal ETL Scripts
# Loads core demo tables in correct order

param()

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Run Minimal ETL - Load Core Tables" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Set location to repo root
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot
Write-Host "[INFO] Working directory: $RepoRoot" -ForegroundColor Green

# Check if venv exists
$VenvPath = Join-Path $RepoRoot "venv"
if (-not (Test-Path $VenvPath)) {
    Write-Host "[ERROR] Virtual environment not found at: $VenvPath" -ForegroundColor Red
    Write-Host "Please create it first: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activate venv
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Green
& "$VenvPath\Scripts\Activate.ps1"

# Define ETL scripts in dependency order
$ETLScripts = @(
    "db\etl\load_categories.py",
    "db\etl\load_geo_zip.py",
    "db\etl\load_customers.py",
    "db\etl\load_sellers.py",
    "db\etl\load_products.py",
    "db\etl\load_orders.py",
    "db\etl\load_order_items.py",
    "db\etl\load_payments.py",
    "db\etl\load_reviews.py"
)

Write-Host "[INFO] Will load $($ETLScripts.Count) core tables" -ForegroundColor Green
Write-Host ""

$SuccessCount = 0
$FailCount = 0

foreach ($script in $ETLScripts) {
    $ScriptName = Split-Path $script -Leaf
    
    if (-not (Test-Path $script)) {
        Write-Host "[WARN] Script not found: $script" -ForegroundColor Yellow
        continue
    }
    
    Write-Host "[$SuccessCount/$($ETLScripts.Count)] Running $ScriptName..." -ForegroundColor Cyan
    
    try {
        $output = & python $script 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] $ScriptName completed successfully" -ForegroundColor Green
            $SuccessCount++
        } else {
            Write-Host "[ERROR] $ScriptName failed!" -ForegroundColor Red
            Write-Host $output -ForegroundColor Red
            $FailCount++
            Write-Host ""
            Write-Host "Stopping ETL pipeline due to failure." -ForegroundColor Red
            break
        }
    } catch {
        Write-Host "[ERROR] Exception running $ScriptName : $_" -ForegroundColor Red
        $FailCount++
        break
    }
    
    Write-Host ""
}

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  ETL Pipeline Complete" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Success: $SuccessCount / Failed: $FailCount" -ForegroundColor $(if ($FailCount -eq 0) { "Green" } else { "Yellow" })
Write-Host ""

if ($FailCount -gt 0) {
    Write-Host "[WARN] Some ETL scripts failed. Check errors above." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "[OK] All ETL scripts completed successfully!" -ForegroundColor Green
}
