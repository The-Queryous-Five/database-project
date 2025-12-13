# 🚀 Quick Start Guide - Olist Analytics Platform (Windows)

**BLG212E Database Management Systems Project**

This guide helps you set up and run the Olist Analytics demo on Windows in ~10 minutes.

---

## 📋 Prerequisites

### Required Software

1. **Python 3.8+**
   - Download: https://www.python.org/downloads/
   - ✅ Check: `python --version`

2. **MySQL 8.0+**
   - Download: https://dev.mysql.com/downloads/installer/
   - Install MySQL Server during setup
   - ✅ Check: MySQL service running in Services panel

3. **Git** (optional, for cloning)
   - Download: https://git-scm.com/download/win

### Optional Tools

- **MySQL Workbench** - Visual database management
- **VS Code** - Code editing with Python extension

---

## 🛠️ Initial Setup (One-Time)

### Step 1: Clone or Download Repository

```powershell
git clone https://github.com/The-Queryous-Five/database-project.git
cd database-project
```

### Step 2: Create Python Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Configure Environment Variables

Create `.env` file in project root:

```powershell
Copy-Item .env.example .env
```

Edit `.env` with your MySQL credentials:

```env
DB_VENDOR=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=olist
DB_USER=root
DB_PASS=YOUR_MYSQL_ROOT_PASSWORD

FLASK_ENV=development
FLASK_APP=app/app.py
```

**Important:** Replace `YOUR_MYSQL_ROOT_PASSWORD` with your actual MySQL root password.

### Step 4: Create Database

```powershell
.\scripts\mysql-create-db.ps1
```

When prompted, enter your MySQL root password.

### Step 5: Apply Database Schema (DDL)

```powershell
.\scripts\apply_ddl_mysql.ps1
```

This creates all tables with the correct structure.

### Step 6: Load Data (ETL)

```powershell
.\scripts\run_etl_minimal.ps1
```

This loads core demo data:
- Categories
- Geolocation
- Customers
- Sellers
- Products
- Orders
- Order Items
- Payments
- Reviews

**Note:** ETL scripts expect CSV data in `db/data/` directory.

### Step 7: Test Database Connection

```powershell
python -m tools.test_db_connection
```

Expected output:
```
[OK] Database connection successful!
Vendor: mysql
Host: 127.0.0.1:3306
Database: olist
```

---

## ▶️ Running the Demo

### Quick Start (One Command)

```powershell
.\scripts\start-servers.ps1
```

This will:
1. ✅ Activate virtual environment
2. ✅ Check required packages
3. ✅ Start Flask backend on http://127.0.0.1:5000
4. ✅ Open frontend in browser

### Manual Start (Alternative)

If you prefer to start services manually:

**Backend:**
```powershell
.\venv\Scripts\Activate.ps1
flask run --host 127.0.0.1 --port 5000
```

**Frontend:**
```powershell
Start-Process "frontend\index.html"
```

---

## 🎯 Using the Application

### Frontend URL
**http://127.0.0.1:5000** (opens in browser automatically)

### Available Features

1. **Customers** 
   - Query by state
   - Top cities by customer count
   - Demo button auto-fills sample values

2. **Orders**
   - Search by customer ID
   - Filter by limit

3. **Products**
   - Top categories
   - Search by name

4. **Payments**
   - Payment statistics
   - Filter by payment type

5. **Reviews**
   - Review statistics
   - Filter by score range

### Using Demo Buttons

Each section has a **"📝 Use demo values"** button:
- Click it to auto-fill sample query parameters
- Automatically runs the query
- Great for quick testing!

---

## 🔧 Troubleshooting

### Port 5000 Already in Use

If another service is using port 5000:

**Option 1: Stop the other service**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Option 2: Change Flask port**

Edit `scripts\start-servers.ps1` and change port 5000 to another port (e.g., 5001).

Also update `frontend\js\config.js`:
```javascript
window.API_BASE_URL = "http://127.0.0.1:5001";
```

### MySQL Connection Failed

**Check MySQL Service:**
```powershell
Get-Service MySQL* | Select-Object Name, Status
```

If stopped:
```powershell
Start-Service MySQL80  # Or your MySQL service name
```

**Verify Credentials:**
1. Open `.env` file
2. Ensure `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS` match your MySQL setup
3. Test connection: `python -m tools.test_db_connection`

**Common MySQL Paths:**
- Service: `C:\Program Files\MySQL\MySQL Server 8.0\`
- Config: `C:\ProgramData\MySQL\MySQL Server 8.0\my.ini`

### Virtual Environment Issues

**Activation failed:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Missing packages:**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### DDL or ETL Fails

**Check logs:**
- DDL errors usually indicate missing database or permissions
- ETL errors often mean missing CSV data files

**Reset database:**
```powershell
# Drop and recreate
mysql -u root -p -e "DROP DATABASE IF EXISTS olist; CREATE DATABASE olist;"

# Reapply DDL
.\scripts\apply_ddl_mysql.ps1
```

### Frontend Shows "Failed to Fetch"

**Backend not running:**
```powershell
# Check if Flask is running
Get-Process python -ErrorAction SilentlyContinue
```

**CORS issues:**
- Backend should have CORS enabled for `http://127.0.0.1`
- Check browser console (F12) for specific errors

**Port mismatch:**
- Verify `frontend\js\config.js` matches actual backend port

---

## 📂 Project Structure

```
database-project/
├── app/                    # Flask backend
│   ├── app.py             # Main Flask application
│   ├── config.py          # Configuration loader
│   ├── db/                # Database connection
│   └── routes/            # API endpoints
├── db/
│   ├── ddl_mysql/         # MySQL table schemas
│   ├── etl/               # Data loading scripts
│   └── data/              # CSV data files (if available)
├── frontend/
│   ├── index.html         # Main UI
│   ├── css/               # Stylesheets
│   └── js/                # JavaScript modules
├── scripts/               # PowerShell automation
├── tools/                 # Utility scripts
├── .env                   # Environment config (create from .env.example)
├── .env.example           # Template
└── requirements.txt       # Python dependencies
```

---

## 🎓 Development Workflow

### Making Changes

1. **Backend changes** (Python):
   - Edit files in `app/`
   - Restart Flask: Ctrl+C in Flask window, then `flask run`

2. **Frontend changes** (HTML/CSS/JS):
   - Edit files in `frontend/`
   - Refresh browser (F5)

3. **Database changes**:
   - Modify DDL in `db/ddl_mysql/`
   - Reapply: `.\scripts\apply_ddl_mysql.ps1`

### Testing

```powershell
# Test database connection
python -m tools.test_db_connection

# Test specific endpoint
Invoke-WebRequest http://127.0.0.1:5000/customers/top-cities?limit=5
```

---

## 📞 Support

### Team Repository
https://github.com/The-Queryous-Five/database-project

### Common Issues
- Check `.env` file exists and has correct MySQL credentials
- Ensure MySQL service is running
- Verify virtual environment is activated
- Check port 5000 is available

### Debug Mode
Run Flask with debug output:
```powershell
$env:FLASK_DEBUG="1"
flask run --host 127.0.0.1 --port 5000
```

---

## ✅ Quick Verification Checklist

Before demo:

- [ ] MySQL service running
- [ ] Database `olist` exists
- [ ] Virtual environment activated
- [ ] `.env` file configured
- [ ] DDL applied (tables created)
- [ ] ETL completed (data loaded)
- [ ] Health check passes: `python -m tools.test_db_connection`
- [ ] Backend starts: `flask run`
- [ ] Frontend opens in browser
- [ ] Demo buttons work

---

**Ready to demo! 🎉**

For detailed API documentation, see `API_ENDPOINTS.md`.
