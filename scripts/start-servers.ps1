# Start Servers Script for Windows
# Starts Flask backend and opens frontend in browser

param()

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Olist Analytics - Starting Servers" -ForegroundColor Cyan
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
    Write-Host "Please create it first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Activate venv
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Green
& "$VenvPath\Scripts\Activate.ps1"

# Check for required packages
Write-Host "[INFO] Checking required Python packages..." -ForegroundColor Green
$RequiredPackages = @("flask", "mysql-connector-python")
$MissingPackages = @()

foreach ($pkg in $RequiredPackages) {
    $check = & python -c "import $($pkg.Replace('-', '_'))" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $MissingPackages += $pkg
    }
}

if ($MissingPackages.Count -gt 0) {
    Write-Host "[WARN] Missing packages: $($MissingPackages -join ', ')" -ForegroundColor Yellow
    
    $RequirementsFile = Join-Path $RepoRoot "requirements.txt"
    if (Test-Path $RequirementsFile) {
        Write-Host "[INFO] Installing from requirements.txt..." -ForegroundColor Green
        & pip install -r $RequirementsFile
    } else {
        Write-Host "[INFO] Installing missing packages..." -ForegroundColor Green
        foreach ($pkg in $MissingPackages) {
            & pip install $pkg
        }
    }
}

# Set Flask environment variables
$env:FLASK_APP = "app/app.py"
$env:FLASK_ENV = "development"

Write-Host ""
Write-Host "[INFO] Starting Flask backend on http://127.0.0.1:5000..." -ForegroundColor Green

# Start Flask in a new window
$FlaskProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$VenvPath\Scripts\Activate.ps1'; `$env:FLASK_APP='app/app.py'; `$env:FLASK_ENV='development'; flask run --host 127.0.0.1 --port 5000" -PassThru -WindowStyle Normal

Write-Host "[OK] Backend started in new window (PID: $($FlaskProcess.Id))" -ForegroundColor Green
Write-Host "[OK] Backend URL: http://127.0.0.1:5000" -ForegroundColor Cyan

# Wait for backend to be ready
Write-Host ""
Write-Host "[INFO] Waiting for backend to start (5 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Open frontend in default browser
$FrontendPath = Join-Path $RepoRoot "frontend\index.html"
$FrontendPath = Resolve-Path $FrontendPath

Write-Host "[INFO] Opening frontend in browser..." -ForegroundColor Green
Start-Process $FrontendPath

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Servers Started Successfully!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Backend:  http://127.0.0.1:5000" -ForegroundColor White
Write-Host "Frontend: $FrontendPath" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C in the Flask window to stop the backend." -ForegroundColor Yellow
Write-Host ""
