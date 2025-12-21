# Apply MySQL DDL Scripts
# Applies all DDL files in the correct order

param()

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Apply MySQL DDL Scripts" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Set location to repo root
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

# Find DDL directory
$DDLDir = $null
if (Test-Path "db\ddl_mysql") {
    $DDLDir = "db\ddl_mysql"
} elseif (Test-Path "db\ddl") {
    $DDLDir = "db\ddl"
} else {
    Write-Host "[ERROR] DDL directory not found!" -ForegroundColor Red
    Write-Host "Expected: db\ddl_mysql or db\ddl" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Found DDL directory: $DDLDir" -ForegroundColor Green

# Common MySQL CLI paths
$MysqlPaths = @(
    "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 9.0\bin\mysql.exe",
    "C:\mysql\bin\mysql.exe",
    "$env:ProgramFiles\MySQL\MySQL Server 8.0\bin\mysql.exe"
)

$MysqlPath = $null
foreach ($path in $MysqlPaths) {
    if (Test-Path $path) {
        $MysqlPath = $path
        break
    }
}

if (-not $MysqlPath) {
    $MysqlPath = (Get-Command mysql -ErrorAction SilentlyContinue).Source
}

if (-not $MysqlPath) {
    Write-Host "[ERROR] MySQL CLI not found!" -ForegroundColor Red
    Write-Host "Please ensure MySQL is installed and in PATH." -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Found MySQL CLI: $MysqlPath" -ForegroundColor Green
Write-Host ""

# Database connection details
$DBHost = "127.0.0.1"
$DBPort = "3306"
$DBUser = "root"
$DBName = "olist"

# Ask for password
Write-Host "Enter MySQL root password:" -ForegroundColor Yellow
$SecurePassword = Read-Host -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecurePassword)
$DBPass = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host ""

# Get all SQL files in order
$SqlFiles = Get-ChildItem -Path $DDLDir -Filter "*.sql" | Sort-Object Name

if ($SqlFiles.Count -eq 0) {
    Write-Host "[WARN] No SQL files found in $DDLDir" -ForegroundColor Yellow
    exit 0
}

Write-Host "[INFO] Found $($SqlFiles.Count) DDL file(s) to apply:" -ForegroundColor Green
foreach ($file in $SqlFiles) {
    Write-Host "  - $($file.Name)" -ForegroundColor White
}
Write-Host ""

# Apply each SQL file
$SuccessCount = 0
$FailCount = 0

foreach ($file in $SqlFiles) {
    Write-Host "[INFO] Applying $($file.Name)..." -ForegroundColor Cyan
    
    $Arguments = @(
        "-h", $DBHost,
        "-P", $DBPort,
        "-u", $DBUser,
        "-D", $DBName
    )
    
    if ($DBPass) {
        $Arguments += "-p$DBPass"
    }
    
    try {
        $output = & $MysqlPath $Arguments -e "source $($file.FullName)" 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] $($file.Name) applied successfully" -ForegroundColor Green
            $SuccessCount++
        } else {
            Write-Host "[ERROR] Failed to apply $($file.Name)" -ForegroundColor Red
            Write-Host $output -ForegroundColor Red
            $FailCount++
        }
    } catch {
        Write-Host "[ERROR] Exception applying $($file.Name): $_" -ForegroundColor Red
        $FailCount++
    }
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  DDL Application Complete" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Success: $SuccessCount / Failed: $FailCount" -ForegroundColor $(if ($FailCount -eq 0) { "Green" } else { "Yellow" })
Write-Host ""

if ($FailCount -gt 0) {
    exit 1
}
