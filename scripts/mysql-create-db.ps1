# MySQL Database Creation Script
# Creates the 'olist' database if it doesn't exist

param()

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  MySQL Database Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Common MySQL CLI paths on Windows
$MysqlPaths = @(
    "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 9.0\bin\mysql.exe",
    "C:\mysql\bin\mysql.exe",
    "$env:ProgramFiles\MySQL\MySQL Server 8.0\bin\mysql.exe",
    "$env:ProgramFiles\MySQL\MySQL Server 8.4\bin\mysql.exe"
)

# Try to find mysql.exe
$MysqlPath = $null
foreach ($path in $MysqlPaths) {
    if (Test-Path $path) {
        $MysqlPath = $path
        break
    }
}

# If not found in common paths, try PATH
if (-not $MysqlPath) {
    $MysqlPath = (Get-Command mysql -ErrorAction SilentlyContinue).Source
}

if (-not $MysqlPath) {
    Write-Host "[ERROR] MySQL CLI not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install MySQL or add it to PATH." -ForegroundColor Yellow
    Write-Host "Common installation path:" -ForegroundColor Yellow
    Write-Host "  C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -ForegroundColor White
    Write-Host ""
    Write-Host "Or install via:" -ForegroundColor Yellow
    Write-Host "  - MySQL Installer: https://dev.mysql.com/downloads/installer/" -ForegroundColor White
    Write-Host "  - Chocolatey: choco install mysql" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "[OK] Found MySQL CLI: $MysqlPath" -ForegroundColor Green
Write-Host ""

# Database connection details
$DBHost = "127.0.0.1"
$DBPort = "3306"
$DBUser = "root"
$DBName = "olist"

# Ask for password securely
Write-Host "Enter MySQL root password (default for local install is often empty or 'root'):" -ForegroundColor Yellow
$SecurePassword = Read-Host -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecurePassword)
$DBPass = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host ""
Write-Host "[INFO] Creating database '$DBName'..." -ForegroundColor Green

# SQL command to create database
$SqlCommand = "CREATE DATABASE IF NOT EXISTS $DBName CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Execute mysql command
$Arguments = @(
    "-h", $DBHost,
    "-P", $DBPort,
    "-u", $DBUser,
    "-e", $SqlCommand
)

if ($DBPass) {
    $Arguments = @("-h", $DBHost, "-P", $DBPort, "-u", $DBUser, "-p$DBPass", "-e", $SqlCommand)
}

try {
    & $MysqlPath $Arguments 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Database '$DBName' created successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Connection details:" -ForegroundColor Cyan
        Write-Host "  Host: $DBHost" -ForegroundColor White
        Write-Host "  Port: $DBPort" -ForegroundColor White
        Write-Host "  User: $DBUser" -ForegroundColor White
        Write-Host "  Database: $DBName" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host "[ERROR] Failed to create database!" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "[ERROR] Failed to execute MySQL command: $_" -ForegroundColor Red
    exit 1
}
